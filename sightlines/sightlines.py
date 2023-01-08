#!/usr/bin/env python

from time import sleep

from launchpad_py import LaunchpadPro  # type: ignore
from sightlines.grid import Grid
from sightlines.cell_runner import CellRunner
from sightlines.updaters.pagerduty import update_pagerduty
from sightlines.updaters.buildkite import update_buildkite
from sightlines.updaters.rainbow import rainbow

hardware = LaunchpadPro()
grid = Grid(hardware=hardware)


def poll_buttons():
    while True:
        button = hardware.ButtonStateXY(mode="pro")
        if button:
            global_x, global_y, velocity = button
            if velocity == 0:
                # This is a button release event, we only care about presses.
                continue

            # Map the global button coordinates to the main grid coordinates.
            grid_x = global_x - 1
            grid_y = global_y - 1
            try:
                cell = grid[grid_x][grid_y]
            except IndexError:
                print("Button press outside of main grid, ignoring.")
                continue
            cell.on_press()

        sleep(0.01)


def main():
    hardware.Open()
    hardware.Reset()

    # The bottom left cell is a smoothly cycling rainbow.
    # This shows that Sightlines is running.
    # Also, it's pretty and calming.
    CellRunner(
        cells=[grid[0][7]],
        function=rainbow,
        interval=0.1,
    )

    # The bottom right cell is a PagerDuty status indicator.
    CellRunner(
        cells=[grid[7][7]],
        function=update_pagerduty,
        interval=30.0,
    )

    # The top 3 rows show the status of Buildkite builds.
    CellRunner(
        cells=grid.get_all_cells_linear()[0:24],
        function=update_buildkite,
        interval=60.0,
    )

    poll_buttons()

if __name__ == "__main__":
    main()

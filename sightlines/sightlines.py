#!/usr/bin/env python

from time import sleep

from launchpad_py import LaunchpadPro  # type: ignore
from sightlines.grid import Grid
from sightlines.cell_runner import CellRunner
from sightlines.updaters.pagerduty import update_pagerduty
from sightlines.updaters.buildkite import update_buildkite
from sightlines.updaters.rainbow import rainbow


def main():
    hardware = LaunchpadPro()
    hardware.Open()
    hardware.Reset()
    grid = Grid(hardware=hardware)
    sleep(5)

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

    while True:
        sleep(1)


if __name__ == "__main__":
    main()

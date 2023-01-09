#!/usr/bin/env python

from time import sleep

from launchpad_py import LaunchpadPro  # type: ignore
from sightlines.grid import Grid
from sightlines.cell_runner import CellRunner
from sightlines.cell_functions.pagerduty import pagerduty_cells
from sightlines.cell_functions.buildkite import pipeline_cells
from sightlines.cell_functions.rainbow import rainbow_cells

launchpad = LaunchpadPro()
grid = Grid(hardware=launchpad)


def main():
    launchpad.Open()
    launchpad.Reset()

    # The bottom left cell is a smoothly cycling rainbow.
    # This shows that Sightlines is running.
    # Also, it's pretty and calming.
    CellRunner(
        cells=[grid[0, 7]],
        function=rainbow_cells,
        interval=0.1,
    )

    # The bottom right cell is a PagerDuty status indicator.
    CellRunner(
        cells=[grid[7, 7]],
        function=pagerduty_cells,
        interval=30.0,
    )

    # The top 3 rows show the status of Buildkite builds.
    CellRunner(
        cells=grid[0:23],
        function=pipeline_cells,
        interval=60.0,
    )

    while True:
        grid.handle_button_event()
        sleep(0.01)


if __name__ == "__main__":
    main()

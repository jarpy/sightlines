#!/usr/bin/env python

"""A Sightlines app that displays status from Buildkite (and PagerDuty)."""

from time import sleep

from launchpad_py import LaunchpadPro  # type: ignore

from sightlines.cell_functions.buildkite import pipeline_cells
from sightlines.cell_functions.pagerduty import pagerduty_cells
from sightlines.cell_functions.rainbow import rainbow_cells
from sightlines.cell_runner import CellRunner
from sightlines.grid import Grid


def main():
    grid = Grid(hardware=LaunchpadPro())

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
        sleep(1)


if __name__ == "__main__":
    main()

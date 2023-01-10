#!/usr/bin/env python

"""A Sightlines app that makes a big, beautiful rainbow."""

from time import sleep

from launchpad_py import LaunchpadPro  # type: ignore

from sightlines.cell_functions.rainbow import rainbow_cells
from sightlines.cell_runner import CellRunner
from sightlines.grid import Grid


def main():
    grid = Grid(hardware=LaunchpadPro())

    CellRunner(cells=grid, function=rainbow_cells, interval=0.1)

    while True:
        sleep(1)


if __name__ == "__main__":
    main()

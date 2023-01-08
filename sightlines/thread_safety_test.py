#!/usr/bin/env python

"""An experiment to see if we can safely use the Launchpad from multiple threads."""
from threading import Thread
from sightlines.grid import Grid
from launchpad_py.launchpad import LaunchpadPro  # type: ignore


def red(grid: Grid):
    while True:
        for cell in grid:
            cell.set_rgb(127, 0, 0)


def green(grid: Grid):
    while True:
        for cell in grid:
            cell.set_rgb(0, 127, 0)


def blue(grid: Grid):
    while True:
        for cell in grid:
            cell.set_rgb(0, 0, 127)


def smoketest():
    hardware = LaunchpadPro()
    hardware.Open()
    hardware.Reset()
    grid = Grid(hardware=hardware)

    threads = [
        Thread(target=red, args=[grid]),
        Thread(target=green, args=[grid]),
        Thread(target=blue, args=[grid]),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    smoketest()

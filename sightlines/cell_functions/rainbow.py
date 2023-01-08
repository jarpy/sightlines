#!/usr/bin/env python

"""Update cells with a cycling rainbow."""
from launchpad_py.launchpad import LaunchpadPro  # type: ignore
from sightlines.cell import Cell
from sightlines.grid import Grid


def rainbow_cells(cells: list[Cell]):
    """A cell function that makes rainbows.

    Each time the function is called, the hue of the cells shifts slightly. Call
    it in a tight loop for a nice animation.
    """
    for index, cell in enumerate(cells):
        current_hue = cell.get_datum("hue")
        if current_hue is None:
            hue = (0 + (5 * index)) % 360
        else:
            hue = current_hue

        hue = (hue + 1) % 360
        cell.set_hls(hue, 30, 127)
        cell.set_datum("hue", hue)


def smoketest():
    hardware = LaunchpadPro()
    hardware.Open()
    hardware.Reset()
    grid = Grid(hardware=hardware)

    while True:
        rainbow_cells(grid.get_all_cells_linear())


if __name__ == "__main__":
    smoketest()

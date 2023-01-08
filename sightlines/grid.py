#!/usr/bin/env python

from sightlines.cell import Cell
from launchpad_py.launchpad import LaunchpadBase, LaunchpadPro  # type: ignore
from typing import cast, Sequence, Union


class Grid:
    """A collection of Cells that make up the main Launchpad grid.

    This excludes the auxiliary buttons on the edges.
    """

    def __init__(self, hardware: LaunchpadBase):
        self.cells = []
        for x in range(8):
            column = []
            for y in range(8):
                column.append(Cell(x + 1, y + 1, hardware=hardware))
            self.cells.append(column)

    def __getitem__(self, index: int) -> Union[Cell, Sequence[Cell]]:
        """Get a cell or sequence of cells from the grid.

        Three operations are supported:

          - Linear indexing: ``grid[0]`` returns the top-left cell.
          - Cartesian indexing: ``grid[7, 7]`` returns the bottom-right cell.
          - Slicing: ``grid[0:15]`` returns the top two rows of cells.
        """
        if isinstance(index, int):
            return self.cells[index % 8][int(index / 8)]

        elif isinstance(index, tuple):
            if len(index) != 2:
                raise ValueError("Cartesian indexing requires exactly 2 coordinates.")
            x, y = index
            return self.cells[x][y]

        elif isinstance(index, slice):
            pointer = index.start
            step = index.step or 1
            cells: list[Cell] = []
            while pointer <= index.stop:
                cells.append(cast(Cell, self[pointer]))
                pointer += step
            return cells

    def __iter__(self):
        """Make the `Grid` iterable.

        Enables ``for cell in grid``, ``list(grid)``.
        """
        return iter(self[0:63])


def smoketest():
    hardware = LaunchpadPro()
    hardware.Open()
    hardware.Reset()
    grid = Grid(hardware=hardware)

    # The whole main grid should light up, and the auxiliary buttons should be off.
    for row in grid.cells:
        for cell in row:
            cell.set_rgb(30, 30, 30)

    # The corners of the grid should be different colors.
    # This demonstrates cartesian addressing.
    grid[0, 0].set_rgb(172, 0, 0)
    grid[0, 7].set_rgb(0, 127, 0)
    grid[7, 0].set_rgb(0, 0, 127)
    grid[7, 7].set_rgb(64, 64, 0)

    # Starting from the top corners, the next 2 cells diagonally towards the
    # center should be pink, indicating that the linear addressing logic is
    # correct.
    grid[9].set_palette_color(59)
    grid[14].set_palette_color(59)

    # Finally, diagonal stripes should be visible in the middle of the device.
    # This demonstrates sliced addressing, including the step parameter.
    for cell in grid[16:47:3]:
        cell.set_palette_color(4)

    for cell in grid[17:47:3]:
        cell.set_palette_color(9)

    for cell in grid[18:47:3]:
        cell.set_palette_color(20)


if __name__ == "__main__":
    smoketest()

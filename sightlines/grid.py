from sightlines.cell import Cell
from launchpad_py.launchpad import LaunchpadBase, LaunchpadPro  # type: ignore


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

    def get_cell(self, x: int, y: int) -> Cell:
        """Get a cell from the grid by its x and y coordinates.

        The coordinates are 0-indexed, and the origin is north-west, so the
        top-left cell is (0, 0).
        """
        return self.cells[x][y]

    def get_cell_linear(self, index: int) -> Cell:
        """Get a cell from the grid by its linear order between 0 and 63.

        Counting starts at the top-left cell, and proceeds left-to-right, then
        top-to-bottom (revealing the English cultural bias of the author).
        """
        return self[index % 8][int(index / 8)]

    def __getitem__(self, column: int) -> list[Cell]:
        """Get a column of cells from the grid by its x coordinate.

        Enables addressing cells with matrix notation, like "grid[3][7]".
        """
        return self.cells[column]


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
    grid.get_cell(0, 0).set_rgb(172, 0, 0)
    grid.get_cell(0, 7).set_rgb(0, 127, 0)
    grid[7][0].set_rgb(0, 0, 127)
    grid[7][7].set_rgb(64, 64, 0)

    # Starting from the top corners, the next 2 cells diagonally towards the
    # center should be pink, indicating that the linear addressing logic is
    # correct.
    grid.get_cell_linear(9).set_palette_color(59)
    grid.get_cell_linear(14).set_palette_color(59)


if __name__ == "__main__":
    smoketest()

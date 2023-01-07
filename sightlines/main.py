from random import randint
from time import sleep

from launchpad_py import LaunchpadPro  # type: ignore
from sightlines.cell import Cell
from sightlines.grid import Grid
from sightlines.cell_runner import CellRunner


def main():
    hardware = LaunchpadPro()
    hardware.Open()
    hardware.Reset()
    grid = Grid(hardware=hardware)

    def updater(cells: list[Cell]):
        for cell in cells:
            cell.set_rgb(randint(0, 127), randint(0, 127), randint(0, 127))

    CellRunner(cells=[grid[7][7]], function=updater, interval=1.0)

    while True:
        sleep(1)

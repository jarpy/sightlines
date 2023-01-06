from random import randint

from launchpad_py import LaunchpadPro
from sightlines.grid import Grid

def main():
    hardware = LaunchpadPro()
    hardware.Open()
    hardware.Reset()
    grid = Grid(hardware=hardware)
    while True:
        for row in grid.cells:
            for cell in row:
                cell.set_rgb(randint(0, 127), randint(0, 127), randint(0, 127))

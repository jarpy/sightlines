from time import sleep

from launchpad_py import LaunchpadPro  # type: ignore
from sightlines.grid import Grid
from sightlines.cell_runner import CellRunner
from sightlines.updaters.pagerduty import update_pagerduty


def main():
    hardware = LaunchpadPro()
    hardware.Open()
    hardware.Reset()
    grid = Grid(hardware=hardware)

    CellRunner(cells=[grid[7][7]], function=update_pagerduty, interval=30.0)

    while True:
        sleep(1)

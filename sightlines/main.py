from time import sleep

from launchpad_py import LaunchpadPro  # type: ignore
from sightlines.grid import Grid
from sightlines.cell_runner import CellRunner
from sightlines.updaters.pagerduty import update_pagerduty
from sightlines.updaters.rainbow import rainbow
from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore


def main():
    hardware = LaunchpadPro()
    hardware.Open()
    hardware.Reset()
    grid = Grid(hardware=hardware)
    sleep(5)

    scheduler = BackgroundScheduler()
    scheduler.start()

    # The bottom right cell is a PagerDuty status indicator.
    CellRunner(
        cells=[grid[7][7]],
        function=update_pagerduty,
        scheduler=scheduler,
        interval=30.0,
    )

    # The bottom left cell is a smoothly cycling rainbow.
    # This shows that Sitelines is running.
    # Also, it's pretty and calming.
    CellRunner(
        cells=[grid[0][7]],
        function=rainbow,
        scheduler=scheduler,
        interval=0.1,
    )

    while True:
        sleep(1)

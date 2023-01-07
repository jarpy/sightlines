from random import randint
from time import sleep
from typing import Callable
from sightlines.cell import Cell
from sightlines.grid import Grid
from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore
from launchpad_py.launchpad import LaunchpadPro  # type: ignore


class CellRunner:
    """A `CellRunner` is responsible updating `Cell`s based on some function.

    Every `interval` seconds, it calls `function` with `cells` as the
    argument.
    """

    def __init__(
        self,
        cells: list[Cell],
        function: Callable[[list[Cell]], None],
        interval: float = 1.0,
    ) -> None:
        self.cells = cells
        self.update_function = function
        self.interval = interval
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            func=self.update_function,
            trigger="interval",
            seconds=self.interval,
            args=[self.cells],
        )
        self.scheduler.start()

    def __del__(self):
        self.scheduler.shutdown()


def smoketest():
    hardware = LaunchpadPro()
    hardware.Open()
    hardware.Reset()
    grid = Grid(hardware=hardware)

    def random_colors(cells: list[Cell]):
        for cell in cells:
            cell.set_rgb(randint(0, 127), randint(0, 127), randint(0, 127))

    left_runner = CellRunner(cells=grid[0], function=random_colors, interval=0.5)
    right_runner = CellRunner(cells=grid[7][3:6], function=random_colors, interval=1.0)

    sleep(5)
    del left_runner
    del right_runner


if __name__ == "__main__":
    smoketest()

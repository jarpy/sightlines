#!/usr/bin/env python

from random import randint
from time import sleep
from typing import Callable, Sequence
from sightlines.cell import Cell
from sightlines.grid import Grid
from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore
from launchpad_py.launchpad import LaunchpadPro  # type: ignore

scheduler = BackgroundScheduler()


class CellRunner:
    """A `CellRunner` is responsible for updating `Cell`s based on some function.

    Every `interval` seconds, it calls `function` with `cells` as the
    argument.
    """

    def __init__(
        self,
        cells: Sequence[Cell],
        function: Callable[[Sequence[Cell]], None],
        interval: float = 1.0,
    ) -> None:
        self.cells = cells
        self.update_function = function
        self.interval = interval
        if not scheduler.running:
            scheduler.start()

        # Run the function once, immediately, to give the user some feedback.
        self.update_function(self.cells)

        # Now schedule it to run periodically.
        self.job = scheduler.add_job(
            func=self.update_function,
            trigger="interval",
            seconds=self.interval,
            args=[self.cells],
            max_instances=1,
            coalesce=True,
        )


def smoketest():
    hardware = LaunchpadPro()
    hardware.Open()
    hardware.Reset()
    grid = Grid(hardware=hardware)

    def random_colors(cells: Sequence[Cell]):
        for cell in cells:
            cell.set_rgb(randint(0, 127), randint(0, 127), randint(0, 127))

    CellRunner(cells=grid[0:23], function=random_colors, interval=0.5)
    CellRunner(cells=grid[40:63], function=random_colors, interval=1.0)

    sleep(5)


if __name__ == "__main__":
    smoketest()

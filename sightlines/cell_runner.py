from typing import Callable
from sightlines.cell import Cell
from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore


class CellRunner:
    """A `CellRunner` is responsible updating `Cell`s based on some function."""

    def __init__(
        self,
        cells: list[Cell],
        update_function: Callable[[list[Cell]], None],
        interval: float = 1.0,
    ) -> None:
        self.cells = cells
        self.update_function = update_function
        self.interval = interval
        self.scheduler = BackgroundScheduler()

    def start(self) -> None:
        """Start the `CellRunner`."""
        self.scheduler.add_job(
            func=self.update_function,
            trigger="interval",
            seconds=self.interval,
            args=[self.cells],
        )
        self.scheduler.start()

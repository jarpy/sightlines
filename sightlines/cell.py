from time import sleep
from typing import Callable
from launchpad_py.launchpad import LaunchpadBase, LaunchpadPro


class Cell:
    """A Cell is a single LED/button on the Launchpad.

    It can be one of the 64 buttons in the main grid, but also be one of the
    auxiliary buttons on the edges.
    """

    # FIXME: Only supports the Launchpad Pro Mk1. Behavior on other models is undefined.
    def __init__(
        self,
        x: int,
        y: int,
        hardware: LaunchpadBase,
    ) -> None:
        self.x = x
        self.y = y
        self.hardware = hardware
        # self.data: dict = {}

    def __repr__(self) -> str:
        return f"Cell(x={self.x}, y={self.y})"

    def set_rgb(self, red: int, green: int, blue: int) -> None:
        self.hardware.LedCtrlXY(
            x=self.x, y=self.y, red=red, green=green, blue=blue, mode="pro"
        )

    # def set_data(self, data: dict) -> None:
    #     self.data = data

    def set_palette_color(self, colorcode: int) -> None:
        self.hardware.LedCtrlXYByCode(
            x=self.x, y=self.y, colorcode=colorcode, mode="pro"
        )

    # def set_pulse(self, colorcode: int) -> None:
    #     self.hardware.LedCtrlPulseXYByCode(x=self.x, y=self.y, colorcode=colorcode)


def smoketest():
    """Smoke test the basic usage of Cells."""
    hardware = LaunchpadPro()
    hardware.Open()
    hardware.Reset()

    # Setting cell colors as RGB values.
    for y in range(10):
        for x in range(10):
            cell = Cell(x=x, y=y, hardware=hardware)
            cell.set_rgb(30, 30, 30)
            sleep(0.01)

    # Setting cell colors from the built in color palette.
    # REF: https://github.com/FMMT666/launchpad.py#color-codes
    cell_number = 0
    for y in range(10):
        for x in range(10):
            cell = Cell(x=x, y=y, hardware=hardware)
            cell.set_palette_color(cell_number)
            cell_number += 1
            sleep(0.01)


if __name__ == "__main__":
    smoketest()

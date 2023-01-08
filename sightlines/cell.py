#!/usr/bin/env python

from time import sleep
from launchpad_py.launchpad import LaunchpadBase, LaunchpadPro  # type: ignore
from colorsys import hls_to_rgb
from typing import Any, Callable


class Cell:
    """A Cell is a single LED/button on the Launchpad.

    It can be one of the 64 buttons in the main grid, but also be one of the
    auxiliary buttons on the edges.

    The `x` and `y` coordinates are the true, physical coordinates on the whole
    device, including any auxiliary buttons. They are not the local coordinates
    of the main grid. The `Grid` class provides an abstraction for the main grid
    coordinates.
    """

    # FIXME: Only supports the Launchpad Pro Mk1. Behavior on other models is undefined.
    def __init__(
        self,
        x: int,
        y: int,
        hardware: LaunchpadBase,
        on_press: Callable[[Any], Any] = lambda self: print(f"No-op: {self}."),
    ) -> None:
        self.x = x
        self.y = y
        self.hardware = hardware
        self.data: dict = {}
        self.on_press_function = on_press

    def __repr__(self) -> str:
        return f"Cell(x={self.x}, y={self.y})"

    def on_press(self) -> None:
        """Call the `on_press_function` of this cell."""
        self.on_press_function(self)

    def set_on_press(self, function: Callable[[Any], Any]) -> None:
        """Set the `on_press_function` of this cell."""
        self.on_press_function = function

    def set_rgb(self, red: int, green: int, blue: int) -> None:
        self.hardware.LedCtrlXY(
            x=self.x, y=self.y, red=red, green=green, blue=blue, mode="pro"
        )

    def set_hls(self, hue, luminance, saturation):
        # Scale the inputs to the range 0-1.
        hue = hue / 360
        luminance = luminance / 127
        saturation = saturation / 127

        # Make the conversion.
        red, green, blue = hls_to_rgb(hue, luminance, saturation)

        # Scale the result back to 0-127, for consumption by the Launchpad.
        red = int(red * 127)
        green = int(green * 127)
        blue = int(blue * 127)

        self.set_rgb(red, green, blue)

    def set_datum(self, key: str, value) -> None:
        """Set a key/value pair in this cell's data store."""
        self.data[key] = value

    def get_datum(self, key: str):
        """Retrieve a keyed value from this cell's data store.

        Returns `None` if the key is not present.
        """
        if key in self.data:
            return self.data[key]
        else:
            return None

    def set_palette_color(self, colorcode: int) -> None:
        self.hardware.LedCtrlXYByCode(
            x=self.x, y=self.y, colorcode=colorcode, mode="pro"
        )
        # In practice, this method seems to be sensitive to aggressive timing.
        # We don't see this with the RGB method. Anyway, a little sleep does a
        # world of good.
        sleep(0.001)

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

"""Update cells with a cycling rainbow."""
from sightlines.cell import Cell


def rainbow(cells: list[Cell]):
    for cell in cells:
        current_hue = cell.get_datum("hue")
        if current_hue is None:
            hue = 0
        else:
            hue = current_hue

        hue = (hue + 1) % 360
        cell.set_hls(hue, 30, 127)
        cell.set_datum("hue", hue)

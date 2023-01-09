# Sightlines

Sightlines is a framework for using a [Novation Launchpad] as an information
display and control panel for general computing tasks.

Sightlines is made possible by the [`launchpad.py`] library, written by @FMMT666.

## Quick Start

- Install Sightlines:  `pip install git+ssh://git@github.com/jarpy/sightlines`
- Run a sample app: `sightlines-rainbow`

## Writing an App (WIP)

### Cell



### Grid

Individual cells are not much fun. The `Grid` class collect all the cells in the main 8x8 grid of the launchpad together. You can then look up cells in various ways.

#### Linear Addressing

#### Cartesian Addressing

#### Slicing

### CellRunner

As a rule, information displays periodically gather some data and then update the display output with what they learned. Sightlines encapsulates this behaviour in the `CellRunner` class. A `CellRunner` takes a collection of cells, and a function. It then periodically calls the function and does whatever is in it, generally setting the color of the cells.

```python
def be_green(cells):
    for cell in cells:
        cell.set_rgb(0, 127, 0)

CellRunner()
```

### Cell Functions


[Novation Launchpad]: https://novationmusic.com/en/launch
[`launchpad.py`]: https://github.com/FMMT666/launchpad.py

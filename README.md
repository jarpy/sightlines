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

All the grid cells are available for lookup by linear index. They are numbered 0 to 63, starting top-left and proceeding left-to right, then top to bottom (revealing the cultural bias of the author).

```python
grid = Grid()
top_left_cell = grid[0]
bottom_right_cell = grid[63]
```

#### Cartesian Addressing

You can use x/y coordinates to get a cell in a more spatial way.

```python
grid = Grid()
top_left_cell = grid[0, 0]
bottom_right_cell = grid[7, 7]
```

#### Slicing

Finally, you can use Python's slicing syntax.

```python
grid = Grid()
second_row = grid[8:15]
```

### CellRunner

As a rule, information displays periodically gather some data and then update the display output with what they learned. Sightlines encapsulates this behaviour in the `CellRunner` class. A `CellRunner` takes a collection of cells, and a function. It then periodically calls the function and does whatever is in it, generally setting the color of the cells.

```python
def be_green(cells):
    for cell in cells:
        cell.set_rgb(0, 127, 0)

CellRunner()
```

### Cell Functions

When you press a cell on the Launchpad, it can do... stuff. 

[Novation Launchpad]: https://novationmusic.com/en/launch
[`launchpad.py`]: https://github.com/FMMT666/launchpad.py

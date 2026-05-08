# Python API

The Python package exposes MISR Toolkit through the `MisrToolkit` module. It is
suited to scripts and array workflows because reads return objects that expose
NumPy-compatible data arrays and map metadata.

## Installation

```bash
python -m pip install -U pip
python -m pip install -U wheel numpy
python -m pip install -U MisrToolkit
```

Source builds require the C toolkit library and HDF-EOS/HDF dependency stack to
be available before building the extension module.

## Core object workflow

The common chained read pattern is:

```python
import MisrToolkit as Mtk

region = Mtk.MtkRegion(37, 40, 42)
data_plane = (
    Mtk.MtkFile(filename)
    .grid("RedBand")
    .field("Red Brf")
    .read(region)
)
array = data_plane.data()
mapinfo = data_plane.mapinfo()
```

The main concepts map closely to the C structures:

| Python concept | Purpose |
| --- | --- |
| `MtkFile` | Open or inspect a MISR product file. |
| `MtkGrid` | Select a grid inside a file. |
| `MtkField` | Select a field inside a grid. |
| `MtkRegion` | Represent a path/block or geographic read region. |
| `MtkDataPlane` | Hold a read two-dimensional data plane and its map metadata. |
| `MtkMapInfo` | Describe the output map, resolution, dimensions, and coordinate transforms. |

## Field slices

Multi-dimensional fields can be addressed with bracket notation in the field
name. For example, `LandHDRF[3][4]` selects a two-dimensional plane from a
higher-dimensional field.

## Useful query functions

The Python module wraps the same functional groups as the C API. Common tasks
include:

- discover grids and fields in a product;
- read file, grid, and field attributes;
- convert latitude/longitude to data-plane line/sample;
- convert line/sample positions back to latitude/longitude;
- compute path and orbit relationships; and
- retrieve pixel time metadata for L1B2 files.

## Legacy reference

The repository includes generated Python interface documentation under
`doc/pymtk/` and a `pymtk.pdf` summary. Treat those generated references as the
complete API index while this Markdown page remains a curated overview.

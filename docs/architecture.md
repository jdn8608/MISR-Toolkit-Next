# Architecture

MISR Toolkit is organized around a C core with optional higher-level bindings
and utilities.

## Layered design

```text
MISR product files (HDF-EOS/HDF)
        │
        ▼
Third-party HDF-EOS, HDF, HDF5, NetCDF, JPEG, zlib libraries
        │
        ▼
MISR Toolkit C core
        │
        ├── Python extension module
        ├── IDL DLM bindings
        └── command-line utilities and examples
```

The toolkit's value is the MISR-specific knowledge built on top of HDF-EOS:
paths, blocks, grids, fields, product metadata, automatic unpacking and
unscaling, coordinate transformations, and time metadata.

## Major functional areas

| Area | Responsibility |
| --- | --- |
| `FileQuery` | Inspect file type, grids, fields, attributes, metadata, path, orbit, block range, and product names. |
| `SetRegion` | Define regions by path/block range, geographic corners, center/extent, or SOM coordinates. |
| `ReadData` | Read regions, blocks, block ranges, raw data, and multi-dimensional field slices. |
| `CoordQuery` | Convert among latitude/longitude, SOM x/y, and block/line/sample coordinates. |
| `MapQuery` | Convert between map line/sample positions and geodetic or SOM coordinates. |
| `OrbitPath` | Resolve path, orbit, block range, and time-range relationships. |
| `UnitConv` | Convert among decimal degrees, DMS, degrees/minutes/seconds, radians, and ISO time. |
| `WriteData` | Write raw binary, 3D binary, and IDL ENVI outputs. |
| `ReProject` | Create geographic grids and resample or transform coordinates. |
| `Regression` | Build and apply regression coefficients and perform simple resampling helpers. |
| `Util` | Toolkit versioning, buffer allocation, and string-list lifecycle helpers. |

## Platform and language support

The legacy documentation describes these support expectations:

- Linux and macOS: C, IDL, and Python from source.
- Windows 64-bit: C, IDL, and Python source support, with some release packages
  containing prebuilt DLLs.

## Generated documentation

The source tree includes a Doxygen configuration template and generated
Doxygen, Python, IDL, and command-line references under `doc/`. This MkDocs tree
should stay concise and maintainable. Use it for conceptual documentation,
installation, tutorials, and curated API summaries; keep generated routine
reference content in generated outputs unless intentionally migrating it.

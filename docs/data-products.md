# Data products

MISR Toolkit works with MISR L1B2, L2, MISR-HR, conventional, and ancillary data
products stored in HDF-EOS/HDF formats.

## Product model

The toolkit presents MISR products through a consistent model:

| Concept | Meaning |
| --- | --- |
| File | A MISR product file with product metadata, path, orbit, and block coverage. |
| Grid | A named gridded collection inside the file, such as `RedBand`. |
| Field | A data variable inside a grid, such as `Red Brf`. |
| Region | A geographic, path/block, or SOM-defined subset to read. |
| Data plane | A two-dimensional read result, possibly selected from a multidimensional field. |
| Map info | Metadata describing the data plane geometry and coordinate transforms. |

## Paths, orbits, and blocks

MISR products are organized using mission-specific path, orbit, and block
concepts. Toolkit query routines can:

- find the path or orbit encoded in a file;
- derive a path from an orbit;
- list orbits for a time range;
- list paths crossing a latitude/longitude or region; and
- determine the block range intersecting a region.

## Coordinates

The toolkit supports conversions among:

- latitude/longitude;
- Space Oblique Mercator (SOM) x/y;
- block/line/sample; and
- output data-plane line/sample.

For supported products, these conversions allow geolocation to be computed
without separate ancillary lookup datasets.

## Reading data

The read routines can automatically stitch blocks and unpack or unscale values.
Use `MtkReadRaw` or equivalent lower-level paths when you need the unmodified raw
stored values.

Multidimensional fields can be read as two-dimensional data planes by specifying
indices in the field name, for example `RetrAppMask[0][5]` or `LandHDRF[3][4]`.

## External data product specification

The legacy docs point users to the MISR Data Product Specification for product
content details. Use that mission-level specification for definitive product
semantics, and use MISR Toolkit docs for how to query and read those products.

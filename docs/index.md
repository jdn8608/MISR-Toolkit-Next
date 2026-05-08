# MISR Toolkit documentation

The MISR Toolkit is a simplified programming interface for working with MISR
L1B2, L2, MISR-HR, conventional, and ancillary products. It is built on
HDF-EOS and adds MISR-aware operations for common data access, geolocation, and
product-query tasks.

Use this MkDocs Material site as the hand-maintainable documentation source for
installation, architecture, interface overviews, data product notes, tutorials,
and development guidance. The generated Doxygen and legacy interface references
remain the authoritative routine-by-routine API details until those references
are migrated into Markdown.

## What the toolkit does

MISR Toolkit can:

- specify read regions by geographic location and extent, or by path and block
  range;
- map between path, orbit, block, time range, and geographic location;
- read MISR data while stitching blocks and unpacking or unscaling values;
- convert coordinates between latitude/longitude, SOM x/y,
  block/line/sample, and data-plane line/sample;
- compute geolocation without ancillary lookup datasets for supported products;
- retrieve pixel acquisition time from L1B2 products;
- read slices from multi-dimensional fields into two-dimensional data planes,
  such as `RetrAppMask[0][5]`; and
- write selected MISR data to IDL ENVI-compatible files.

!!! note "ENVI projection support"
    The legacy Doxygen front page notes that recent ENVI versions no longer
    support SOM projections. Confirm your downstream tool support before
    relying on ENVI output for SOM-projected data.

## Start here

- [Getting started](getting-started.md) explains the main user paths.
- [Installation](installation.md) covers Python binaries and source builds.
- [Architecture](architecture.md) describes the C core and language bindings.
- [Python API](python-api.md) and [C API](c-api.md) summarize the two primary
  programming interfaces.
- [Data products](data-products.md) explains how the toolkit views MISR files,
  grids, fields, paths, blocks, and metadata.
- [Tutorials](tutorials/index.md) collects short task-oriented examples.
- [Dependency modernization](development/dependencies.md) records the current
  native-library and Python compatibility baseline for maintainers.

## Legacy references

The source tree still includes generated and legacy documentation under `doc/`:

- Doxygen C documentation and routine summary pages.
- `Mtk_ug.pdf`, the MISR Toolkit User's Guide.
- `pymtk.pdf` and generated Python binding pages.
- IDL and command-line utility reference pages.

When these docs are published to GitHub Pages, the MkDocs site is the entry
point. Keep detailed generated API reference content in Doxygen until it is
intentionally converted into Markdown.

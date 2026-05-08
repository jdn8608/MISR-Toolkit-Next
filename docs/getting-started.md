# Getting started

MISR Toolkit supports several ways to work with MISR products. Choose the path
that matches your environment and the level of control you need.

## Choose an interface

| Interface | Best for | Notes |
| --- | --- | --- |
| Python | Interactive analysis, notebooks, scripts, and array workflows. | Python wheels are the easiest installation path when available. |
| C | Native applications, batch processing, and binding development. | The C library is the core implementation and exposes the complete routine set. |
| IDL | Existing IDL science workflows. | Binary DLM packages have historically been published for releases. |
| Command-line utilities | File inspection and conversion tasks. | See the legacy command utility reference in generated docs. |

## Typical workflow

1. Install MISR Toolkit and its dependencies.
2. Identify the input MISR file, grid, and field.
3. Define a region by path/block range or geographic coordinates.
4. Read the data into a data plane.
5. Use the returned map information for coordinate conversion, geolocation, and
   downstream processing.

## Python quick start

```python
import os
import MisrToolkit as Mtk

region = Mtk.MtkRegion(37, 40, 42)
filename = os.path.join(
    os.environ["MTKHOME"],
    "..",
    "Mtk_testdata",
    "in",
    "MISR_AM1_GRP_ELLIPSOID_GM_P037_O029058_AA_F03_0024.hdf",
)

data_plane = (
    Mtk.MtkFile(filename)
    .grid("RedBand")
    .field("Red Brf")
    .read(region)
)
array = data_plane.data()
mapinfo = data_plane.mapinfo()
```

## C quick start

```c
#include "MisrToolkit.h"

MTKt_Region region = MTKT_REGION_INIT;
MTKt_DataBuffer databuf = MTKT_DATABUFFER_INIT;
MTKt_MapInfo mapinfo = MTKT_MAPINFO_INIT;

MtkSetRegionByLatLonExtent(32.2, -114.5, 200.0, 100.0, "km", &region);
MtkReadData(filename, "RedBand", "Red Brf", region, &databuf, &mapinfo);

/* Use databuf and mapinfo here. */

MtkDataBufferFree(&databuf);
```

## Where to go next

- For binary and source setup, see [Installation](installation.md).
- For data model concepts, see [Data products](data-products.md).
- For interface-specific notes, see [Python API](python-api.md) and
  [C API](c-api.md).

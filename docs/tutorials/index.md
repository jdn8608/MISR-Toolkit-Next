# Tutorials

This section collects short task-oriented examples. Keep examples compact and
copyable; link to generated reference material for exhaustive parameter lists.

## Read a field in Python

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

plane = Mtk.MtkFile(filename).grid("RedBand").field("Red Brf").read(region)
values = plane.data()
mapinfo = plane.mapinfo()
```

## Read a geographic region in C

```c
MTKt_Region region = MTKT_REGION_INIT;
MTKt_DataBuffer databuf = MTKT_DATABUFFER_INIT;
MTKt_MapInfo mapinfo = MTKT_MAPINFO_INIT;

MtkSetRegionByLatLonExtent(32.2, -114.5, 200.0, 100.0, "km", &region);
MtkReadData(filename, "RedBand", "Red Brf", region, &databuf, &mapinfo);

MtkDataBufferFree(&databuf);
```

## Convert coordinates

After reading a data plane, use its map information to convert between map
line/sample and geodetic coordinates:

```c
float line;
float sample;
double lat;
double lon;

MtkLatLonToLS(mapinfo, 32.2, -114.5, &line, &sample);
MtkLSToLatLon(mapinfo, line, sample, &lat, &lon);
```

## Query orbit and path relationships

Use the `OrbitPath` routine family when you need to discover files or coverage
from time and location constraints. Common tasks include resolving an orbit to a
path, listing orbits in a time range, and finding paths crossing a region.

## Add more tutorials

Good tutorial pages should include:

- a short goal statement;
- prerequisites and required sample data;
- a minimal working example;
- expected output or checks; and
- links to the relevant API overview pages.

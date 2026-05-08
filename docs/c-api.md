# C API

The C library is the core MISR Toolkit interface. All higher-level bindings are
built on top of it or follow its data model.

## Include and status handling

C programs generally include the toolkit headers, create initialized toolkit
structures, call routines that return `MTKt_status`, and free allocated buffers
when finished.

```c
#include "MisrToolkit.h"
#include "MisrError.h"

MTKt_Region region = MTKT_REGION_INIT;
MTKt_DataBuffer databuf = MTKT_DATABUFFER_INIT;
MTKt_MapInfo mapinfo = MTKT_MAPINFO_INIT;

MTKt_status status = MtkSetRegionByLatLonExtent(
    32.2, -114.5, 200.0, 100.0, "km", &region
);

status = MtkReadData(filename, "RedBand", "Red Brf", region, &databuf, &mapinfo);

MtkDataBufferFree(&databuf);
```

## Routine families

The generated Doxygen routine table groups the C API into these families:

| Family | Representative routines | Summary |
| --- | --- | --- |
| Util | `MtkVersion`, `MtkDataBufferAllocate`, `MtkDataBufferFree` | Version and buffer lifecycle helpers. |
| FileQuery | `MtkFileType`, `MtkFileToPath`, `MtkFileToGridList`, `MtkTimeMetaRead` | File, metadata, grid, field, path, orbit, and time metadata queries. |
| UnitConv | `MtkDdToRad`, `MtkDmsToDd`, `MtkJulianToDateTime` | Unit and time-format conversions. |
| CoordQuery | `MtkLatLonToBls`, `MtkLatLonToSomXY`, `MtkPixelTime` | MISR path/block/SOM/geodetic coordinate conversions. |
| MapQuery | `MtkLatLonToLS`, `MtkLSToLatLon`, `MtkCreateLatLon` | Data-plane map coordinate conversions. |
| OrbitPath | `MtkOrbitToPath`, `MtkTimeRangeToOrbitList` | Orbit, path, and time-range relationships. |
| SetRegion | `MtkSetRegionByLatLonExtent`, `MtkSetRegionByPathBlockRange` | Region construction. |
| ReadData | `MtkReadData`, `MtkReadBlock`, `MtkReadRaw` | MISR data reads. |
| WriteData | `MtkWriteBinFile`, `MtkWriteEnviFile` | Export helpers. |
| ReProject | `MtkCreateGeoGrid`, `MtkResampleNearestNeighbor` | Reprojection and resampling support. |
| Regression | `MtkRegressionCoeffCalc`, `MtkApplyRegression` | Regression and smoothing helpers. |

## Memory ownership

- Initialize toolkit structures with their `MTKT_*_INIT` macros when available.
- Free data buffers with the matching toolkit free routine.
- Free toolkit string lists with `MtkStringListFree`.
- Check each returned `MTKt_status` before using output values.

## Generated reference

Use the generated Doxygen documentation for complete signatures, structure
fields, and routine-level details. The source files `doc/functable.dox` and
`doc/mainpage.dox` are the current source material for the C routine summary and
front page content.

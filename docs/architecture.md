# Architecture

MISR Toolkit is organized around a C library that knows how to inspect MISR
HDF-EOS/HDF products, translate MISR path/block/grid conventions, read and
write typed data planes, and expose the same capabilities through optional
language bindings and command-line utilities.

## Layered design

```text
MISR product files (HDF-EOS/HDF)
        │
        ▼
Native dependencies: HDF-EOS, HDF4, HDF5, NetCDF, GCTP, JPEG, zlib, math/dl
        │
        ▼
MISR Toolkit C core: libMisrToolkit.{a,so}
        │
        ├── command-line utilities in bin/
        ├── Python extension package: wrappers/python
        ├── IDL DLM wrapper: wrappers/idl
        └── Ruby extension/gem wrapper: wrappers/ruby
```

The toolkit's central value is the MISR-specific layer above HDF-EOS: product
metadata conventions, paths, orbits, blocks, grids, fields, region selection,
automatic data conversion, map metadata, geolocation, and time metadata.

## Module map

The root `Makefile` builds the public C library from these module directories
plus the internal `misrcoord` and `odl` support libraries. The table below maps
source-tree modules to their primary responsibility and the public header, when
one is present.

| Module | Public header or entry point | Responsibility |
| --- | --- | --- |
| `ReadData` | `ReadData/include/MisrReadData.h` | Reads grids/fields from product files by region, block, or block range; includes product-specific readers, raw reads, conversion helpers, and cache support. |
| `WriteData` | `WriteData/include/MisrWriteData.h` | Writes toolkit data buffers as binary, 3D binary, or ENVI-style outputs. |
| `CoordQuery` | `CoordQuery/include/MisrCoordQuery.h` | Converts among latitude/longitude, SOM x/y, and block/line/sample coordinates; derives path projection parameters, block corners, and pixel time. |
| `MapQuery` | `MapQuery/include/MisrMapQuery.h` | Converts between map line/sample positions and lat/lon or SOM coordinates; creates latitude/longitude arrays and generic or GCTP map-info structures. |
| `OrbitPath` | `OrbitPath/include/MisrOrbitPath.h` | Resolves relationships among path, orbit, time ranges, geographic regions, and block ranges. |
| `SetRegion` | `SetRegion/include/MisrSetRegion.h` | Constructs `MtkRegion` values from path/block ranges, geographic corners, lat/lon extents, SOM corners, and generic map information. |
| `FileQuery` | `FileQuery/include/MisrFileQuery.h` | Inspects file type, local granule ID, version, fill values, attributes, grids, fields, dimensions, data types, metadata, path, orbit, block range, filenames, and time metadata. |
| `UnitConv` | `UnitConv/include/MisrUnitConv.h` | Converts angular units among decimal degrees, degrees/minutes/seconds, DMS, and radians. |
| `Regression` | `Regression/include/MisrRegression.h` | Allocates, computes, resamples, applies, and frees regression coefficients; includes smoothing, downsample, and mask upsample helpers. |
| `ReProject` | `ReProject/include/MisrReProject.h` | Creates geographic grids, transforms coordinate arrays, and resamples data with nearest-neighbor or cubic-convolution methods. |
| `Util` | `Util/include/MisrUtil.h` | Provides versioning, data-buffer allocation/import/free routines, string-list lifecycle helpers, field-name parsing, HDF-to-toolkit data-type conversion, calendar/Julian/TAI/UTC conversion, and NetCDF variable lookup helpers. |
| `misrcoord` | `misrcoord/misrproj.h` | Internal MISR SOM projection implementation used by coordinate and map routines. |
| `odl` | `odl/odldef.h`, parser sources | Internal Object Description Language parser/formatter used for metadata-label handling. |

## Public API boundaries

### C API

The C API is the stable core boundary. Consumers include the aggregate header
`include/MisrToolkit.h` and the module headers listed above. The build produces
`lib/libMisrToolkit.a` and `lib/libMisrToolkit.so`, backed by module objects and
the `misrcoord` and `odl` support objects. Public C routines use the `Mtk*`
naming convention and exchange toolkit structures such as regions, data buffers,
map information, projection parameters, time metadata, and string lists.

### Python extension

The Python boundary is a CPython extension built from `wrappers/python/setup.py`.
It packages an extension module named `MisrToolkit.MisrToolkit` plus the
`MisrToolkit` Python package. The extension links against the C library and the
same native HDF/HDF-EOS dependency stack; it exposes object-oriented wrappers for
files, grids, fields, regions, data planes, map info, projection parameters,
regression coefficients, and selected module-level query/conversion functions.

### Command-line tools

The command-line boundary is a set of small executables generated from selected
`src/Mtk*.c` command sources. Both `Makefile` and `SConstruct` enumerate tools
for file queries, coordinate conversions, orbit/path queries, unit conversions,
region/block queries, read operations, and metadata extraction. The
`applications/` directory also contains higher-level programs such as
reprojection and surface-BRF regression applications that link against the
installed C library.

### IDL and Ruby wrappers

The IDL boundary is a DLM built from `wrappers/idl/idl_mtk.c` with a generated
`lib/idl_MisrToolkit.dlm` descriptor and IDL environment helper files. The Ruby
boundary lives under `wrappers/ruby`; it contains a native extension, Ruby
classes for files/grids/fields/regions/data planes/coordinates, tests, RDoc
output, and a historical gem artifact. These wrappers should be treated as
separate compatibility surfaces because they bind directly to native libraries
and runtime-specific extension APIs.

## Build systems currently present

| Build system | Location | Current role |
| --- | --- | --- |
| Root Make build | `Makefile`, `common.mk` | Primary legacy build. Detects Linux/macOS architecture, sets compiler and dependency flags, includes module `module.mk` files, builds static/shared libraries, command utilities, applications, tests, IDL wrapper, Python wrapper, docs, install and distribution outputs. |
| SCons build | `SConstruct`, module `SConscript` files | Alternative build for the C library, command utilities, install outputs, tests, docs, tags, selected dependencies, `misrcoord`, `odl`, and the IDL wrapper. |
| Module make fragments | `*/module.mk` | Per-module source/header manifests included by the root `Makefile`; present for `Util`, `FileQuery`, `UnitConv`, `CoordQuery`, `MapQuery`, `OrbitPath`, `SetRegion`, `ReadData`, `WriteData`, `ReProject`, `Regression`, `misrcoord`, and `odl`. |
| Visual Studio projects | `win32/MisrToolkit/**/*.vcproj`, `win32/MisrToolkit/**/*.vcxproj`, `win64/MisrToolkit/**/*.vcxproj` | Windows project files for the C library, command/toolkit executable, Python wrapper, IDL wrapper, tests, and examples. |
| Wrapper-specific builds | `wrappers/python/setup.py`, `wrappers/ruby/src/ext/extconf.rb`, `wrappers/ruby/src/Makefile` | Runtime-specific native-extension builds layered on top of the C library and native dependencies. |

## Data flow

The common read/geolocation workflow is:

```text
product file
  └─ FileQuery opens/inspects file metadata
      └─ grid selection
          └─ field selection
              └─ SetRegion / OrbitPath / FileQuery define region or block range
                  └─ ReadData returns an MtkDataBuffer data plane
                      └─ MapQuery / CoordQuery / ReProject provide map info and geolocation
```

In prose:

1. A MISR product file is identified and inspected for product type, path, orbit,
   block range, grids, fields, dimensions, data types, fill values, and metadata.
2. A caller selects a grid and field, optionally checking native field names or
   field dimensions.
3. A caller defines a region directly, derives a block range from the file, or
   asks orbit/path routines to intersect time, region, path, and block concepts.
4. `ReadData` reads the requested field over the selected region/block range into
   a typed data buffer/data plane.
5. `MapQuery`, `CoordQuery`, and `ReProject` attach map information,
   line/sample-to-geolocation conversions, SOM coordinates, latitude/longitude
   arrays, or resampled/reprojected output planes.

## Modernization implications

The architecture has a compact conceptual core, but modernization work should
preserve the C ABI deliberately because command-line tools and all wrappers sit
on top of it. Build consolidation should account for the external native stack,
per-module manifests, Windows project files, and runtime extension APIs rather
than treating the repository as a pure C package or a pure Python package.

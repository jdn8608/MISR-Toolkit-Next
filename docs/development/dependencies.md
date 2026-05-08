# Dependency modernization

This page records the dependency baseline for modern MISR Toolkit builds and the
migration path away from the oldest bundled third-party sources. It is intended
for maintainers updating build scripts, wheels, and platform packages.

## Minimum supported dependency versions

The versions below are the minimum versions to support for new development and
packaging work. The legacy source helper scripts may still download older
known-good inputs for historical release reproduction, but new validation should
start from this baseline.

| Dependency | Minimum supported version | Notes |
| --- | --- | --- |
| HDF4 | 4.2.15 | Last HDF4 release line commonly packaged by scientific distributions; required by HDF-EOS2. |
| HDF5 | 1.10.11 | Prefer an actively packaged 1.10+ ABI. HDF5 1.8.x remains legacy-only. |
| HDF-EOS2 | 2.20 | Use the HDF4-based HDF-EOS2 library. Validate against newer EOSDIS HDF-EOS2 releases before raising this floor. |
| netCDF-C | 4.9.2 | Use the C library and headers; avoid depending on the obsolete netCDF interfaces bundled inside HDF4. |
| zlib | 1.2.13 | Older zlib builds may work, but 1.2.13+ is the practical security and packaging floor. |
| JPEG/libjpeg-turbo | libjpeg-turbo 2.1.5 or IJG JPEG v9e | The toolkit only needs the libjpeg-compatible C ABI used by HDF4. libjpeg-turbo is preferred where available. |
| NumPy | 1.23.5 | Minimum for source builds of the Python extension. NumPy 2.x should be treated as a validation target before publishing binary wheels built against it. |

## Platform install paths

The build still discovers native dependencies from environment variables first.
Use these locations as the expected defaults when documenting installations or
adding package-manager automation.

| Platform | Package-manager paths | Recommended custom prefix | Environment variables to set |
| --- | --- | --- | --- |
| Linux | `/usr/include`, `/usr/lib`, `/usr/lib64`, Debian/Ubuntu multiarch paths such as `/usr/lib/x86_64-linux-gnu`, and conda prefixes under `$CONDA_PREFIX/include` and `$CONDA_PREFIX/lib` | `/opt/misr-deps` or `/usr/local/hdfeoslibs` | `HDFEOS_INC`, `HDFEOS_LIB`, `HDFINC`, `HDFLIB`, `HDF5INC`, `HDF5LIB`, `NCINC`, `NCLIB`, `JPEGINC`, `JPEGLIB`, `GCTPINC`, `GCTPLIB` |
| macOS | Homebrew on Apple Silicon under `/opt/homebrew/include` and `/opt/homebrew/lib`; Homebrew on Intel under `/usr/local/include` and `/usr/local/lib`; conda under `$CONDA_PREFIX/include` and `$CONDA_PREFIX/lib` | `/opt/misr-deps` or `/usr/local/hdfeoslibs` | Same variables as Linux. Prefer explicit variables because Homebrew does not provide HDF-EOS2. |
| Windows | Legacy repository binaries under `win64/`; conda-forge libraries under `%CONDA_PREFIX%\Library\include` and `%CONDA_PREFIX%\Library\lib`; vcpkg libraries under the selected triplet prefix | `%LOCALAPPDATA%\misr-deps` for manual builds | Same variable names can be set in PowerShell with `$env:NAME = "path"`. If none are set, `wrappers/python/setup.py` falls back to `win64/`. |

## Conda-forge feasibility assessment

Conda-forge is the strongest candidate for a modern cross-platform dependency
story because it already has the core scientific C stack used by MISR Toolkit:
HDF4, HDF5, netCDF-C, zlib, libjpeg-turbo or compatible JPEG packages, and
NumPy. A conda-forge recipe for MISR Toolkit is feasible if maintainers solve
the HDF-EOS2 packaging gap and verify the exact HDF4/HDF-EOS2 link order on all
target platforms.

Recommended conda-forge approach:

1. Add or refresh an HDF-EOS2 feedstock that links to conda-forge HDF4, zlib,
   JPEG, and any required GCTP components.
2. Build the MISR Toolkit C library against conda-forge native packages in the
   `host` environment.
3. Build the Python extension with NumPy in both `host` and `run` requirements,
   using conda-forge's NumPy pinning policy for ABI-compatible wheels or conda
   packages.
4. Test Linux x86_64/aarch64, macOS arm64/x86_64, and Windows x86_64 before
   advertising the recipe as the preferred installation path.

Until HDF-EOS2 is reliably packaged, conda-forge should be documented as
"promising but not the default" rather than the primary user workflow.

## Homebrew feasibility assessment for macOS

Homebrew is useful for HDF5, netCDF-C, zlib, and libjpeg-turbo on macOS, but it
is not yet a complete MISR Toolkit dependency provider because HDF4 and
HDF-EOS2 availability can lag or require custom taps. Homebrew also installs
into different prefixes on Apple Silicon and Intel Macs, so build instructions
must avoid hard-coded `/usr/local` paths.

Recommended Homebrew approach:

```bash
brew install hdf5 netcdf zlib libjpeg-turbo pkgconf
export HDF5INC="$(brew --prefix hdf5)/include"
export HDF5LIB="$(brew --prefix hdf5)/lib"
export NCINC="$(brew --prefix netcdf)/include"
export NCLIB="$(brew --prefix netcdf)/lib"
export JPEGINC="$(brew --prefix libjpeg-turbo)/include"
export JPEGLIB="$(brew --prefix libjpeg-turbo)/lib"
```

HDF4 and HDF-EOS2 should be installed from a custom prefix, conda environment,
or future tap formula until Homebrew provides reliable formulae for both. For
macOS maintainers, conda-forge is likely a lower-maintenance route than a
Homebrew-only installation.

## Windows bundled binaries policy

The `win64/` directory should be retained for now, updated before any new binary
release, and eventually replaced by package-manager or CI-built artifacts.

| Decision | Rationale |
| --- | --- |
| Retain short term | `wrappers/python/setup.py` uses `win64/` as the fallback when no native dependency environment variables are set, so removing it would break current Windows source builds. |
| Update before publishing new wheels | The bundled HDF5 1.8.x and older netCDF/HDF-EOS libraries are below the modernization baseline. Refreshing them reduces security and compiler-compatibility risk. |
| Replace long term | Committed binary dependency trees are hard to audit and update. Prefer conda-forge packages, vcpkg ports, or a CI job that downloads verified vendor archives and publishes build artifacts. |

## Compatibility matrix

Use this matrix for CI planning and release qualification. "Required" rows are
the minimum support promise; "target" rows are the combinations maintainers
should validate before a release if resources are available.

| Tier | Python | Operating systems | Compilers | NumPy | Native libraries |
| --- | --- | --- | --- | --- | --- |
| Required source build | 3.10, 3.11, 3.12 | Linux x86_64, macOS arm64/x86_64, Windows 10/11 x86_64 | GCC 10+, Clang 13+, MSVC 2019+ | 1.23.5 through latest 1.26.x | HDF4 4.2.15, HDF5 1.10.11+, HDF-EOS2 2.20+, netCDF-C 4.9.2+, zlib 1.2.13+, libjpeg-turbo 2.1.5+ or IJG JPEG v9e+ |
| Target source build | 3.13 | Linux x86_64/aarch64, macOS arm64/x86_64, Windows 11 x86_64 | GCC 12+, Apple Clang 15+, MSVC 2022+ | Latest NumPy 2.x | Same native minimums, plus latest packaged HDF5/netCDF-C releases where ABI-compatible |
| Legacy reproduction | 2.7 and 3.6-3.9 | CentOS 7-era Linux, macOS 10.14, Windows 10 | Legacy GCC/Clang/MSVC matching released binaries | 1.15+ for historical Python wheels | HDF-EOS2 2.18, HDF4 4.2.10, HDF5 1.8.16, netCDF-C 4.4.0, zlib 1.2.5, IJG JPEG v6b |
| Unsupported | Python 2.7 for new releases | 32-bit platforms and end-of-life operating systems | Compilers without C99 support | NumPy versions older than 1.23.5 for new Python packages | Native dependency builds older than the modernization baseline except for historical reproduction |

## Packaging follow-up checklist

- Add CI jobs that build the C library and Python extension against conda-forge
  dependencies on Linux, macOS, and Windows.
- Replace hard-coded Windows fallback paths with a documented dependency-prefix
  discovery mechanism once an external Windows dependency provider is selected.
- Raise or lower the NumPy floor only after compiling and importing the extension
  against each supported Python version.
- Keep `README`, `docs/installation.md`, and Python packaging metadata in sync
  with this page whenever the compatibility matrix changes.

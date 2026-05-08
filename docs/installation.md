# Installation

MISR Toolkit depends on the HDF-EOS/HDF stack and related compression and data
libraries. Python users also need NumPy. For the current dependency baseline,
platform paths, package-manager assessment, and compatibility matrix, see
[Dependency modernization](development/dependencies.md).

## Supported platforms

The modern support target is:

- Linux x86_64 source builds with GCC 10 or newer;
- macOS arm64 and x86_64 source builds with Clang 13 or newer;
- Windows 10/11 x86_64 source builds with MSVC 2019 or newer; and
- Python 3.10, 3.11, and 3.12 for new Python package builds.

The legacy README and Doxygen front page also describe historical testing on
CentOS 7, macOS 10.14.6, Windows 10, and Python 2.7/3.6-era binaries. Those
combinations are useful for reproducing old releases, but they are not the
modern baseline for new packages.

## Python binary installation

For Python users, the most convenient path is the published wheel from PyPI:

```bash
python -m pip install -U pip
python -m pip install -U wheel "numpy>=1.23.5"
python -m pip install -U MisrToolkit
```

Downloadable wheel distributions may also be attached to GitHub releases. If a
wheel is unavailable for your Python or operating system, build from source with
the native dependency stack installed first.

## Native dependency locations

The legacy build discovers native libraries from environment variables. The
recommended custom prefix remains `/usr/local/hdfeoslibs` for shared multi-user
Linux/macOS systems, but conda and Homebrew prefixes are also valid when the
matching libraries are available.

Common locations are:

| Platform | Common dependency locations |
| --- | --- |
| Linux | `/usr/include`, `/usr/lib`, `/usr/lib64`, `/usr/lib/x86_64-linux-gnu`, `$CONDA_PREFIX/include`, `$CONDA_PREFIX/lib`, `/opt/misr-deps`, `/usr/local/hdfeoslibs` |
| macOS | `/opt/homebrew/include`, `/opt/homebrew/lib`, `/usr/local/include`, `/usr/local/lib`, `$CONDA_PREFIX/include`, `$CONDA_PREFIX/lib`, `/usr/local/hdfeoslibs` |
| Windows | `win64/` fallback libraries, `%CONDA_PREFIX%\Library\include`, `%CONDA_PREFIX%\Library\lib`, vcpkg triplet prefixes, `%LOCALAPPDATA%\misr-deps` |

Set these variables when dependencies are not installed in a compiler default
search path:

```bash
export HDFEOS_INC=/path/to/include
export HDFEOS_LIB=/path/to/lib
export HDFINC=/path/to/include
export HDFLIB=/path/to/lib
export HDF5INC=/path/to/include
export HDF5LIB=/path/to/lib
export NCINC=/path/to/include
export NCLIB=/path/to/lib
export JPEGINC=/path/to/include
export JPEGLIB=/path/to/lib
export GCTPINC=/path/to/include
export GCTPLIB=/path/to/lib
```

## Source installation on Linux and macOS

A typical legacy source build is:

```bash
mkdir Mtk_tmp
cd Mtk_tmp
tar xzvf Mtk-src-1.5.X.tar.gz
tar xzvf Mtk-testdata-1.5.X.tar.gz
cd Mtk-src-1.5.X
scripts/download_libraries
sudo scripts/install_hdf+hdfeos
source /usr/local/hdfeoslibs/bin/hdfeos_env.sh
export MTK_INSTALLDIR=/usr/local/Mtk-1.5.X
make
make testall
sudo make install
```

For a non-root install, choose a writable dependency prefix and omit `sudo`.
When building IDL support, set `IDL_DIR` before building. When testing only part
of the project, use the more specific make targets documented in
[Development](development.md).

## Python source build

The Python package has a `pyproject.toml` build-system declaration so pip can
install build requirements, including NumPy, before running `setup.py`:

```bash
cd wrappers/python
python -m pip install --upgrade pip build wheel
python -m pip install .
```

The Python extension still links to the native MISR Toolkit and HDF-EOS/HDF
libraries. Build and install the C library first, then set the dependency
environment variables if the headers and libraries are outside default compiler
paths.

## Third-party dependency baseline

New development and packaging work should use the modernization baseline below:

| Dependency | Minimum for new packages |
| --- | --- |
| HDF-EOS2 | 2.20 |
| HDF4 | 4.2.15 |
| HDF5 | 1.10.11 |
| netCDF-C | 4.9.2 |
| JPEG/libjpeg-turbo | libjpeg-turbo 2.1.5 or IJG JPEG v9e |
| zlib | 1.2.13 |
| NumPy | 1.23.5 |

The legacy helper scripts still download older known-good source inputs for
historical release reproduction: HDF-EOS2 2.18v1.00, HDF4 4.2.10, HDF5 1.8.16,
netCDF-C 4.4.0, JPEG v6b, and zlib 1.2.5. Prefer the modern baseline unless you
are intentionally reproducing an old release.

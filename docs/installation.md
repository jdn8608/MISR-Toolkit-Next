# Installation

MISR Toolkit depends on the HDF-EOS/HDF stack and related compression and data
libraries. Python users also need NumPy.

## Supported platforms noted by the legacy docs

The existing README and Doxygen front page describe testing on:

- Linux CentOS 7 or later;
- macOS 10.14.6 or later; and
- Windows 10 64-bit.

The core interface is C. Python and IDL bindings are also available. Python 2.7
support is deprecated because Python 2.7 has reached end of life.

## Python binary installation

For Python users, the most convenient path is the published wheel from PyPI:

```bash
python -m pip install -U pip
python -m pip install -U wheel numpy
python -m pip install -U MisrToolkit
```

Downloadable wheel distributions may also be attached to GitHub releases.

## IDL binary installation

IDL Dynamically Loadable Module distributions may be attached to releases. After
extracting the package, configure IDL so it can find the DLM, either by setting
`IDL_DLM_PATH` or by using IDL's `PREF_SET` workflow described in the release
README.

## Source installation on Linux and macOS

The legacy build expects HDF-EOS/HDF libraries and MISR Toolkit to be installed
in predictable locations. The recommended defaults are:

- HDF-EOS/HDF libraries: `/usr/local/hdfeoslibs`
- MISR Toolkit: `/usr/local/Mtk-1.5.X`

Custom locations are supported. Installing into `/usr/local` usually requires
root or `sudo` privileges.

A typical source build is:

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

## Third-party dependencies

The legacy documentation lists these dependency versions as known-good source
inputs:

| Dependency | Version noted in legacy docs |
| --- | --- |
| HDF-EOS | 2.18v1.00 |
| HDF4 | 4.2.10 |
| HDF5 | 1.8.16 |
| NetCDF | 4.4.0 |
| JPEG | jpegsrc.v6b |
| zlib | 1.2.5 |
| NumPy | 1.15 or later |

Prefer the repository's `scripts/download_libraries` and
`scripts/install_hdf+hdfeos` helpers because they apply compatibility patches
needed by some platforms.

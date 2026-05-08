from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as _build_ext
import os
import platform
from pathlib import Path


WRAPPER_DIR = Path(__file__).resolve().parent
MTK_SOURCE_ROOT = Path(os.getenv("MTK_SOURCE_ROOT", WRAPPER_DIR / "../..")).resolve()


def source_path(*parts):
    return str(MTK_SOURCE_ROOT.joinpath(*parts))


mtk_include_dirs = [source_path("include"), source_path("Regression", "include"),
                source_path("ReProject", "include"), source_path("WriteData", "include"),
                source_path("ReadData", "include"), source_path("SetRegion", "include"),
                source_path("OrbitPath", "include"), source_path("MapQuery", "include"),
                source_path("CoordQuery", "include"), source_path("UnitConv", "include"),
                source_path("FileQuery", "include"), source_path("Util", "include")]

hdfeosinc = os.getenv('HDFEOS_INC')
hdfeoslib = os.getenv('HDFEOS_LIB')
gctpinc = os.getenv('GCTPINC', default=os.getenv('HDFEOS_INC'))
gctplib = os.getenv('GCTPLIB', default=os.getenv('HDFEOS_LIB'))
ncinc = os.getenv('NCINC', default=os.getenv('HDFEOS_INC'))
nclib = os.getenv('NCLIB', default=os.getenv('HDFEOS_LIB'))
jpeginc = os.getenv('JPEGINC', default=os.getenv('HDFEOS_INC'))
jpeglib = os.getenv('JPEGLIB', default=os.getenv('HDFEOS_LIB'))
hdf5inc = os.getenv('HDF5INC', default=os.getenv('HDFEOS_INC'))
hdf5lib = os.getenv('HDF5LIB', default=os.getenv('HDFEOS_LIB'))
hdfinc = os.getenv('HDFINC')
hdflib = os.getenv('HDFLIB')


if platform.system() == "Windows":
    mtk_extra_object = [source_path('win64', 'MisrToolkit', 'x64', 'Release', 'MisrToolkit_bundled.lib')]
    mtk_libraries = []
    if not (gctpinc or gctplib or ncinc or nclib or jpeginc or jpeglib or
            hdf5inc or hdf5lib or hdfeosinc or hdfeoslib or hdfinc or hdflib):
        hdfinc = source_path("win64", "HDF_4.2.14", "include")
        hdflib = source_path("win64", "HDF_4.2.14", "lib")
        jpeginc = hdfinc
        jpeglib = hdflib
        hdfeosinc = source_path("win64", "hdfeos_2.19", "include")
        hdfeoslib = source_path("win64", "hdfeos_2.19", "lib")
        gctpinc = hdfeosinc
        gctplib = hdfeoslib
        ncinc = source_path("win64", "netcdf_4.7.4", "include")
        nclib = source_path("win64", "netcdf_4.7.4", "lib")
        hdf5inc = source_path("win64", "HDF5_1.8.21", "include")
        hdf5lib = source_path("win64", "HDF5_1.8.21", "lib")
else:
    mtk_libraries = ['netcdf', 'hdf5_hl', 'hdf5', 'hdfeos', 'Gctp', 'mfhdf', 'df', 'jpeg', 'z', 'm']
    mtk_extra_object = [source_path('lib', 'libMisrToolkit.a')]


def present(paths):
    return [path for path in paths if path]


module = Extension('MisrToolkit',
	include_dirs = present([ ncinc, hdf5inc, jpeginc, gctpinc,
                     hdfeosinc, hdfinc, jpeginc ]) + mtk_include_dirs,
	library_dirs = present([ '.', nclib, hdf5lib, hdfeoslib,
                     gctplib, hdflib, jpeglib ]),
    libraries = mtk_libraries,
    extra_objects = mtk_extra_object,
    sources = ['pyMtkBlockCorners.c', 'pyMtkDataPlane.c', 'pyMtkField.c', 'pyMtkFile.c',
               'pyMtkFileId.c', 'pyMtkGeoBlock.c', 'pyMtkGeoCoord.c', 'pyMtkGeoRegion.c',
               'pyMtkGrid.c', 'pyMtkMapInfo.c', 'pyMtkProjParam.c', 'pyMtkReProject.c',
               'pyMtkRegCoeff.c', 'pyMtkRegion.c', 'pyMtkRegression.c', 'pyMtkSomCoord.c',
               'pyMtkSomRegion.c', 'pyMtkTimeMetaData.c', 'pycoordquery.c', 'pyfilequery.c',
               'pyhelpers.c', 'pymisrtoolkit.c', 'pyorbitpath.c', 'pyunitconv.c', 'pyutil.c'],
    )



class build_ext(_build_ext):
    def finalize_options(self):
        super().finalize_options()

        # Import NumPy only after the PEP 517 backend has installed the
        # build-system requirements declared in pyproject.toml.
        import numpy

        for extension in self.extensions:
            extension.include_dirs.insert(0, numpy.get_include())


setup (packages = ['MisrToolkit'],
       ext_package = 'MisrToolkit',
       ext_modules = [module],
       cmdclass={'build_ext': build_ext})

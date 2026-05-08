# Modernization audit

This audit captures the current modernization risks and decisions that should be
resolved before replacing or consolidating build, packaging, and wrapper systems.
It is intentionally scoped to repository structure and public-interface planning,
not to a full source-level API review.

## Current surfaces to preserve or retire

| Surface | Current implementation | Modernization question |
| --- | --- | --- |
| C library | Root `Makefile`, `SConstruct`, module `module.mk`/`SConscript` manifests, public headers, `libMisrToolkit` outputs | Is the C ABI the primary long-term contract, and should it gain versioned symbol/ABI checks? |
| Python extension | `wrappers/python/setup.py` CPython extension linked to `libMisrToolkit` and HDF/HDF-EOS libraries | Should packaging move to `pyproject.toml` and binary wheels, and which Python/NumPy ABI range is supported? |
| Command-line tools | Root `Makefile` and `SConstruct` generate `bin/Mtk*` utilities from selected command sources | Should these remain first-class deliverables, and should their output/exit behavior be regression-tested? |
| IDL wrapper | `wrappers/idl/idl_mtk.c`, generated DLM file, IDL test scripts, Windows IDL project files | Should IDL remain supported, be community-maintained, or be archived as legacy? |
| Ruby wrapper | `wrappers/ruby` native extension, Ruby classes, tests, generated docs, historical gem | Should Ruby remain supported, be community-maintained, or be archived as legacy? |
| Windows deliverables | Visual Studio solutions/projects and checked-in third-party Windows dependency trees | Should Windows continue as source-only support, binary distribution support, or best-effort community support? |

## Modernization risk list

### Native dependencies

The toolkit depends on a large native geospatial/scientific stack: HDF-EOS,
HDF4, HDF5, NetCDF, GCTP, JPEG, zlib, and platform math/dynamic-loader
libraries. The existing build scripts rely heavily on environment variables such
as `HDFEOS_INC`, `HDFEOS_LIB`, `HDFINC`, `HDFLIB`, `HDF5INC`, `HDF5LIB`,
`NCINC`, `NCLIB`, `GCTPINC`, `GCTPLIB`, `JPEGINC`, and `JPEGLIB`.
Modernization risk is high because dependency discovery, library naming,
transitive link order, and license/distribution constraints differ across Linux,
macOS, and Windows.

Mitigations to consider:

- Document a single supported dependency installation path per operating system.
- Add configure-time diagnostics that report missing headers and libraries with
  actionable messages.
- Decide whether binary packages bundle native dependencies or require external
  installation.
- Add CI jobs that build from clean dependency installs rather than local
  developer machines.

### Python C API

The Python extension is a CPython C extension with NumPy include usage and direct
links to the C library/native dependency stack. Modernization risk is medium to
high because Python minor-version support, NumPy ABI changes, wheel policy,
Windows import libraries, and reference-counting errors can break builds or
runtime imports even when the C library compiles.

Mitigations to consider:

- Define supported Python versions and NumPy version policy before changing the
  build backend.
- Add import smoke tests and wrapper API tests to CI for every supported Python.
- Consider whether the extension should target the stable Python ABI, stay on the
  regular CPython API, or move some binding code to a generator/tooling approach.

### Binary packaging

The repository has legacy install/distribution targets, wrapper-specific build
scripts, platform project files, and checked-in Windows dependency artifacts.
Modernization risk is high because C libraries, command-line tools, Python
wheels, IDL DLMs, Ruby gems, and Windows installers have different artifact
formats and dependency-bundling expectations.

Mitigations to consider:

- Split packaging goals into source distribution, C install tree, Python wheel,
  and optional wrapper artifacts.
- Define artifact names, versioning, and compatibility tags.
- Decide whether packages are built only by CI and whether reproducible builds
  are required.

### Test data availability

Many useful tests require MISR product samples and the historical toolkit test
data tree. Modernization risk is high because public CI may not have access to
large or restricted data files, while unit tests without realistic product data
may miss HDF-EOS integration regressions.

Mitigations to consider:

- Inventory tests that require external product data versus pure unit tests.
- Create a minimal public fixture set if licensing and file size allow it.
- Mark integration tests so contributors can run them locally without making CI
  mandatory for every large-data scenario.
- Capture expected command-line outputs for representative products.

### Windows support

The repository contains Visual Studio project files, Windows-specific dependency
folders, installer scripts, and Python/IDL project files. Modernization risk is
high because current Unix Make/SCons logic and Windows project maintenance can
drift, and binary compatibility depends on compiler version, architecture,
runtime library choice, and third-party DLL availability.

Mitigations to consider:

- Decide whether supported Windows means source builds, CI-built binaries,
  Python wheels, installers, or only archived legacy projects.
- If Windows remains supported, add CI with the chosen Visual Studio version and
  an explicit dependency acquisition strategy.
- Remove or clearly quarantine stale binary dependencies only after a replacement
  path exists.

## Decisions needed

| Decision | Options to choose among | Why it matters |
| --- | --- | --- |
| Supported operating systems | Linux only; Linux and macOS; Linux/macOS/Windows; tiered support with primary and best-effort platforms | Determines CI matrix, dependency instructions, packaging formats, and whether Visual Studio projects stay maintained. |
| Supported Python versions | Current CPython releases only; long-term enterprise versions; source-only for older versions; wheels for selected versions | Determines CPython API compatibility, NumPy policy, wheel tags, and test matrix size. |
| Retain IDL wrapper? | Fully supported; community-maintained; frozen legacy; removed in a major release | Determines whether IDL runtime access, DLM generation, tests, docs, and Windows IDL projects need modernization. |
| Retain Ruby wrapper? | Fully supported; community-maintained; frozen legacy; removed in a major release | Determines whether the native Ruby extension, gemspec, tests, docs, and dependency on NArray/Ruby C API need maintenance. |
| Keep SCons? | Keep as a supported build; keep temporarily during migration; replace with one canonical build; remove after parity is proven | Determines whether every source list and install/test target must continue to be maintained in both Make/SCons and any new build system. |

## Recommended next audit steps

1. Inventory public C functions and structures from installed headers, then tag
   each as stable, deprecated, internal-but-exported, or wrapper-only.
2. Build a dependency matrix for Linux, macOS, and Windows showing header paths,
   library names, runtime library names, and license/distribution constraints.
3. Classify tests into pure unit, native-dependency integration, product-data
   integration, wrapper import/API, and command-line behavior tests.
4. Draft a deprecation policy for wrappers and build systems before deleting any
   legacy project or generated artifact.
5. Choose one canonical developer build path and keep compatibility builds only
   where a named maintainer or CI job verifies them.

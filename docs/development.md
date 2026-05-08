# Development

This page summarizes contributor tasks for the documentation and legacy build
system.

## Build the MkDocs site locally

Install MkDocs Material and build the site:

```bash
python -m pip install mkdocs-material
mkdocs build --strict
```

For live preview while editing:

```bash
mkdocs serve
```

The generated site is written to `site/`, which should not be committed.

## GitHub Pages deployment

The repository includes a GitHub Actions workflow that builds the MkDocs site
with `mkdocs build --strict`, uploads the generated `site/` artifact, and deploys
it with GitHub Pages.

After the workflow is merged, configure the repository's Pages settings to use
**GitHub Actions** as the Pages source.

## Legacy C build targets

The top-level `Makefile` contains targets for the C library, bindings, tests,
Doxygen docs, and distribution packages. Common targets include:

| Target | Purpose |
| --- | --- |
| `make` | Build the default toolkit outputs. |
| `make test` | Run C tests. |
| `make testpython` | Run Python tests. |
| `make testidl` | Run IDL tests. |
| `make testall` | Run C, Python, and IDL tests. |
| `make doc` | Generate legacy documentation when Doxygen and other tools are available. |
| `make clean` | Remove build outputs. |

Some tests require the MISR testdata package and configured external
dependencies.


## Python wrapper packaging

The Python wrapper is a PEP 517 project rooted at `wrappers/python`. Static
package metadata and build requirements live in `wrappers/python/pyproject.toml`;
`setup.py` remains responsible for declaring the native extension module.

Before building Python distributions, configure the HDF-EOS/HDF environment and
build the native MISR Toolkit library from the repository root:

```bash
make lib
export MTK_SOURCE_ROOT=$PWD
```

`MTK_SOURCE_ROOT` lets PEP 517 isolated builds locate the already-built native
MISR Toolkit library and headers, including when `python -m build` builds the
wheel from the source distribution. Then build and smoke-install the Python
wheel from the wrapper directory:

```bash
cd wrappers/python
python -m pip install -U build
python -m build
python -m pip install --force-reinstall dist/*.whl
```

For legacy in-tree wrapper builds and tests, the top-level Makefile targets are
still available:

```bash
make python
make testpython
```

Some Python tests require the MISR testdata package and configured external
dependencies.

## Documentation maintenance guidelines

- Keep Markdown pages concise, task-oriented, and reviewed by maintainers.
- Do not paste large generated reference tables into Markdown unless the source
  of truth is intentionally moved.
- Prefer links or short summaries for Doxygen, IDL, Python-generated, and PDF
  references.
- Update `mkdocs.yml` navigation whenever adding or renaming a page.
- Run `mkdocs build --strict` before opening a pull request.

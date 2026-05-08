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

## Documentation maintenance guidelines

- Keep Markdown pages concise, task-oriented, and reviewed by maintainers.
- Do not paste large generated reference tables into Markdown unless the source
  of truth is intentionally moved.
- Prefer links or short summaries for Doxygen, IDL, Python-generated, and PDF
  references.
- Update `mkdocs.yml` navigation whenever adding or renaming a page.
- Run `mkdocs build --strict` before opening a pull request.

## Dependency modernization

Dependency policy, package-manager feasibility notes, Windows binary guidance,
and the compatibility matrix are maintained in
[Dependency modernization](development/dependencies.md). Update that page along
with `README`, `docs/installation.md`, and Python packaging metadata whenever a
minimum supported dependency changes.

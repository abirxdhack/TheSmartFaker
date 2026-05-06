"""
SmartFaker documentation compiler.

Walks the live :mod:`smartfaker` package and emits per-method and
per-function reStructuredText pages under ``docs/source/api/``. Inspired by
the Pyrogram/Irenogram docs build system, the compiler is intentionally
self-contained and zero-dependency beyond the standard library plus the
package itself, so it can run inside CI before Sphinx.

Run as::

    python -m compiler.docs.compiler

or via the project Makefile target::

    make docs
"""

import ast
import importlib
import inspect
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = Path(__file__).resolve().parent / "template"
API_DEST = ROOT / "docs" / "source" / "api"

INTERNAL_NAMES = {
    "Faker",
}


def _load_template(name: str) -> str:
    """Return the raw text of a docs template by file name."""
    with open(TEMPLATE_DIR / name, encoding="utf-8") as fh:
        return fh.read()


def _slug(name: str) -> str:
    """Return a hyphen-cased slug suitable for use in RST file names."""
    cleaned = re.sub(r"[^0-9a-zA-Z_]+", "_", name).strip("_")
    return cleaned.replace("_", "-").lower()


def _public_methods(cls) -> list:
    """Return the sorted list of public method names declared on ``cls``.

    Only methods physically defined on ``cls`` (not inherited from
    :class:`object`) and whose names do not start with an underscore are
    returned. Both regular and async coroutine methods are included.
    """
    names = []
    for name, member in inspect.getmembers(cls):
        if name.startswith("_"):
            continue
        if not (inspect.isfunction(member) or inspect.iscoroutinefunction(member)):
            continue
        qualname = getattr(member, "__qualname__", "")
        if not qualname.startswith(cls.__name__ + "."):
            continue
        names.append(name)
    return sorted(set(names))


def _public_functions(module) -> list:
    """Return the sorted list of public function names declared in ``module``.

    Filters out re-exports, dunder names and module-level helpers whose name
    starts with an underscore.
    """
    names = []
    for name, member in inspect.getmembers(module):
        if name.startswith("_"):
            continue
        if not (inspect.isfunction(member) or inspect.iscoroutinefunction(member)):
            continue
        if getattr(member, "__module__", "") != module.__name__:
            continue
        names.append(name)
    return sorted(set(names))


def _write(path: Path, content: str) -> None:
    """Create parent directories and write ``content`` to ``path`` as UTF-8."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def _build_method_pages(methods, dest_dir: Path) -> list:
    """Emit one RST page per method and return their toctree-ready stems."""
    template = _load_template("method.txt")
    stems = []
    for method in methods:
        stem = _slug(method)
        title = "{}()".format(method)
        body = template.format(
            title=title,
            title_markup="=" * len(title),
            method=method,
        )
        _write(dest_dir / "{}.rst".format(stem), body)
        stems.append(stem)
    return stems


def _build_function_pages(functions, dest_dir: Path) -> list:
    """Emit one RST page per IBAN helper and return their toctree stems."""
    template = _load_template("function.txt")
    stems = []
    for func in functions:
        stem = _slug(func)
        title = "{}()".format(func)
        body = template.format(
            title=title,
            title_markup="=" * len(title),
            function=func,
        )
        _write(dest_dir / "{}.rst".format(stem), body)
        stems.append(stem)
    return stems


def _format_index(template_name: str, items, stems, dest_dir_name: str) -> str:
    """Render a category index page from ``template_name``."""
    template = _load_template(template_name)
    hlist = "\n    ".join(
        "- :doc:`{name}() <{slug}>`".format(name=name, slug=stem)
        for name, stem in zip(items, stems)
    )
    toctree = "\n    ".join(stems)
    return template.format(hlist=hlist, toctree=toctree)


def _build_countries_page(faker, country_generators) -> None:
    """Emit the supported-countries reference page."""
    template = _load_template("countries.txt")
    address_rows = "\n".join(
        "    * - {code}\n      - {name}".format(
            code=item["country_code"], name=item["country_name"]
        )
        for item in faker.countries()
    )
    iban_rows = "\n".join(
        "    * - {code}\n      - {name}".format(
            code=item["country_code"], name=item["country_name"]
        )
        for item in faker.iban_countries()
    )
    body = template.format(address_rows=address_rows, iban_rows=iban_rows)
    _write(API_DEST / "countries.rst", body)


def _validate_with_ast() -> None:
    """Lightweight syntax check ensuring the package files are parseable."""
    for relpath in ("smartfaker/__init__.py", "smartfaker/fake.py", "smartfaker/iban.py"):
        with open(ROOT / relpath, encoding="utf-8") as fh:
            ast.parse(fh.read())


def main() -> int:
    """Compile every documentation artifact under ``docs/source/api/``."""
    sys.path.insert(0, str(ROOT))
    _validate_with_ast()

    smartfaker = importlib.import_module("smartfaker")
    iban_module = importlib.import_module("smartfaker.iban")
    faker_cls = getattr(smartfaker, "Faker")

    methods = _public_methods(faker_cls)
    functions = _public_functions(iban_module)

    method_stems = _build_method_pages(methods, API_DEST / "methods")
    function_stems = _build_function_pages(functions, API_DEST / "iban")

    methods_index = _format_index(
        "methods_index.txt", methods, method_stems, "methods"
    )
    iban_index = _format_index(
        "iban_index.txt", functions, function_stems, "iban"
    )

    _write(API_DEST / "methods" / "index.rst", methods_index)
    _write(API_DEST / "iban" / "index.rst", iban_index)

    faker_instance = faker_cls()
    country_generators = getattr(iban_module, "COUNTRY_GENERATORS")
    _build_countries_page(faker_instance, country_generators)

    sys.stdout.write(
        "Generated {} method pages, {} IBAN function pages and the "
        "countries reference under {}\n".format(
            len(method_stems), len(function_stems), API_DEST.relative_to(ROOT)
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

Data Model
==========

SmartFaker stores its bundled data as plain JSON files inside
``smartfaker/data/`` — one file per ISO 3166-1 alpha-2 country code (with
the United Kingdom stored as ``uk.json`` for legacy reasons and surfaced as
``GB`` in :meth:`~smartfaker.Faker.countries`).

Each JSON file contains a JSON array of address records. The exact field
set varies by country (it mirrors the upstream open data we sourced), but
typical keys include ``person_name``, ``street``, ``city``, ``zip`` /
``postal_code``, ``state``, ``phone``, and ``country_code``.

Loading
-------

At construction time, :class:`~smartfaker.Faker` walks ``smartfaker/data/``
and loads every ``*.json`` file into the in-memory ``data`` mapping
(``code -> list[record]``). Files that fail JSON parsing are silently
skipped so a single broken file cannot prevent the rest from loading.

The library prefers :func:`importlib.resources.files` for resource access
to remain compatible with zipped wheels and editable installs, falling
back to :mod:`pathlib` when running on older Python versions.

Country code normalisation
--------------------------

- Input is case-insensitive.
- ``uk`` is normalised internally; the public surface always reports
  ``GB`` per ISO 3166-1.
- ``country_flag`` is derived from the *uppercase* country code as a pair
  of regional-indicator code points.

Memory footprint
----------------

A loaded :class:`~smartfaker.Faker` instance holds the full dataset in
memory. Reuse a single instance across requests in a long-running process
to avoid the reload cost.

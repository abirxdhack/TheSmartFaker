Changelog
=========

This page lists notable changes. The authoritative changelog lives at
https://github.com/abirxdhack/TheSmartFaker/releases.

4.0.0
-----

- Public API now exposes both **sync** primaries (``address``,
  ``batch_addresses``, ``iban``) **and** ``a``-prefixed async coroutines
  (``aaddress``, ``abatch_addresses``, ``aiban``).
- IBAN module helpers gained async wrappers
  (``acalculate_check_digits``, ``avalidate_iban``, ``agenerate_*``).
- Async methods dispatch through :func:`asyncio.to_thread` to keep the
  event loop free.
- Documentation rewritten with full intro / tutorials / examples /
  advanced / API sections.
- Backwards-compatible ``address_sync`` / ``iban_sync`` aliases retained.

3.x
---

- Async-first API with ``_sync`` wrappers.
- 200+ countries of bundled address data.
- 57 country IBAN generators with MOD-97 validation.

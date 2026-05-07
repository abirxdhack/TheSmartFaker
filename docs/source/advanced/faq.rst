FAQ
===

Is the data real?
-----------------

The bundled records are sourced from open address datasets and shipped as
plain JSON. They are intended for **testing and demos** — do **not** use
them as if they identified real people.

Are the IBANs real?
-------------------

The IBANs are *structurally* valid (correct country format, correct MOD-97
check digits) and the bank codes are drawn from real well-known issuers
where possible. They are **not** linked to real bank accounts and must
never be used for actual transfers.

Why both ``address`` and ``aaddress``?
--------------------------------------

So both call sites work without ceremony. Sync apps call ``address``;
async apps call ``aaddress``. Both share the same signature and return
shape.

How do I make output deterministic in tests?
--------------------------------------------

Seed :mod:`random` before constructing the :class:`~smartfaker.Faker`
instance::

    import random
    random.seed(42)

Why is the wheel a few MB?
--------------------------

The bundled per-country JSON files account for almost all of it. The
trade-off is zero network calls at runtime.

How can I add a country?
------------------------

Drop a ``smartfaker/data/<code>.json`` file containing a list of address
dicts and the loader picks it up automatically. For IBAN support, add a
country format to ``country_data`` and a ``generate_<code>`` function in
``smartfaker/iban.py``, then wire it into ``COUNTRY_GENERATORS``.

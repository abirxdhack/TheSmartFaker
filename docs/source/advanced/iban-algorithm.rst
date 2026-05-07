IBAN Algorithm
==============

SmartFaker implements the ISO 13616 standard for IBAN generation.

Structure
---------

An IBAN is composed of:

1. **Country code** — 2 uppercase letters
2. **Check digits** — 2 numeric digits
3. **BBAN** — country-specific Basic Bank Account Number

Generation flow
---------------

1. The country-specific BBAN generator produces a BBAN of the documented
   length (``COUNTRY_GENERATORS[code]["length"]`` minus four).
2. :func:`~smartfaker.iban.calculate_check_digits` computes the MOD-97
   check digits.
3. The candidate IBAN is assembled and re-validated with
   :func:`~smartfaker.iban.validate_iban` before being returned.

MOD-97 check
------------

For check-digit calculation, the temporary string is constructed as
``BBAN + country + "00"``. Each letter is replaced with its numeric
equivalent (``A=10, B=11, …, Z=35``), the result is interpreted as one
big integer, and the check digits are ``98 - (n mod 97)`` (zero-padded).

Validation reverses the construction: ``BBAN + country + check`` mod 97
must equal ``1``.

Country-specific quirks
-----------------------

- **Italy / San Marino** — the BBAN starts with a CIN check character
  computed from a 26-element weight table.
- **Belgium** — the BBAN ends with two check digits derived from the bank
  code + account number using mod-97.
- **France / Monaco** — include a 2-digit numeric *key* after the account.
- **Germany / UK / US** — the bank code is selected from a curated list
  of well-known real bank codes for realism.

The full per-country layout is encoded in ``country_data`` inside
:mod:`smartfaker.iban` — read the source for the exact field order.

Response Schema
===============

Address response
----------------

Each address dict contains country-specific fields plus three guaranteed
metadata keys:

================  ===============================================
Key               Description
================  ===============================================
``api_owner``     Attribution string — ``"@ISmartCoder"``
``api_updates``   Update channel — ``"t.me/TheSmartDev"``
``country_flag``  Regional-indicator emoji flag (e.g. ``"🇺🇸"``)
================  ===============================================

Country-specific fields commonly include ``person_name``, ``street``,
``city``, ``state`` / ``region``, ``zip`` / ``postal_code``, ``phone``,
``country_code``. Use ``fields=[...]`` to project only the keys you want.

IBAN response
-------------

==================  =====================================================
Key                 Description
==================  =====================================================
``iban``            Full IBAN string
``country``         ISO alpha-2 country code
``valid``           Always ``True`` (re-checked with MOD-97 before return)
``length``          Total length of the IBAN
``details``         Parsed BBAN sub-fields (see below)
``api_owner``       Attribution
``api_updates``     Update channel
==================  =====================================================

``details`` always contains ``bban`` and ``check_digits``, plus any of
``bank_code``, ``branch_code``, ``sort_code``, ``prefix``, ``type_code``,
``identification_number``, ``key``, ``account_type``, ``owner_type``,
``reserved``, ``account_number`` and ``cin`` depending on the country
format.

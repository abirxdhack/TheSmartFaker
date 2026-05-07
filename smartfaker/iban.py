"""IBAN generation utilities for SmartFaker.

Provides country-specific IBAN (International Bank Account Number) generation
logic, bank code data, country format specifications, and BBAN generator
functions for each supported country.

All public helpers are synchronous. ``a``-prefixed coroutine wrappers
(:func:`acalculate_check_digits`, :func:`avalidate_iban`,
:func:`agenerate_numeric`, :func:`agenerate_alpha`, :func:`agenerate_alphanum`)
are provided for use inside ``asyncio`` event loops without blocking.

Supported countries: AT, AZ, BH, BE, BA, BR, CZ, DK, DO, SV, EE, FO, FI, FR,
GE, DE, GI, GL, GT, HU, IS, IE, IT, JO, KZ, XK, KW, LV, LB, LI, LT, LU, MK,
MT, MR, MC, ME, NO, PK, PL, QA, MD, RO, SM, SA, RS, SK, ES, CH, TH, TR, UA,
AE, GB, US, VA, VG.

Example — sync::

    from smartfaker.iban import COUNTRY_GENERATORS, calculate_check_digits, validate_iban

    bban = COUNTRY_GENERATORS["DE"]["generator"]()
    check = calculate_check_digits("DE", bban)
    iban = f"DE{check}{bban}"
    print(iban, validate_iban(iban))

Example — async::

    import asyncio
    from smartfaker.iban import acalculate_check_digits, avalidate_iban

    async def main():
        check = await acalculate_check_digits("DE", "370400440532013000")
        ok = await avalidate_iban(f"DE{check}370400440532013000")
        print(check, ok)

    asyncio.run(main())
"""

import asyncio
import random
import string

bank_codes_data = {
    "AT": ["12000", "20151"],
    "AZ": ["NABZ", "AIIB"],
    "BH": ["BBKU", "AUBB"],
    "BE": ["001", "310"],
    "BA": ["129", "199"],
    "BR": ["00000000", "00360305", "33700394", "60394079", "60701190", "07237373", "04902979", "00000208"],
    "CZ": ["0100", "0800"],
    "DK": ["0040", "0321"],
    "DO": ["BAGR", "BRES"],
    "SV": ["CENR", "CUSC"],
    "EE": ["10", "22"],
    "FO": ["6460", "9182"],
    "FI": ["123456", "789012"],
    "FR": ["30003", "30004"],
    "GE": ["NB", "BG"],
    "DE": ["10010010", "12030000", "20030700", "37050198", "50010517"],
    "GI": ["NWBK", "BARC"],
    "GL": ["6471", "9183"],
    "GT": ["TRAJ", "GTCO"],
    "HU": ["117", "120"],
    "IS": ["0159", "0300"],
    "IE": ["AIBK", "BOFI"],
    "IT": ["05428", "01030"],
    "JO": ["CBJO", "JIBA"],
    "KZ": ["125", "135"],
    "XK": ["1212", "1505"],
    "KW": ["CBKU", "GULB"],
    "LV": ["HABA", "UNLA"],
    "LB": ["0001", "0002"],
    "LI": ["08810", "08811"],
    "LT": ["70440", "71800"],
    "LU": ["001", "002"],
    "MK": ["250", "300"],
    "MT": ["MALT", "MMEB"],
    "MR": ["00001", "00002"],
    "MC": ["30003", "30004"],
    "ME": ["505", "510"],
    "NO": ["1503", "8601"],
    "PK": ["SCBL", "HABB"],
    "PL": ["10100055", "10200002", "11400009", "12400001", "11600006"],
    "QA": ["QNBA", "DOHB"],
    "MD": ["AG", "VI"],
    "RO": ["AAAA", "BRDE"],
    "SM": ["05428", "01030"],
    "SA": ["10", "40"],
    "RS": ["260", "265"],
    "SK": ["1100", "0200"],
    "ES": ["2100", "2085"],
    "CH": ["00700", "00800"],
    "TH": ["002", "004", "006", "014", "025", "069", "073"],
    "TR": ["00061", "00134"],
    "UA": ["300346", "300536"],
    "AE": ["033", "040"],
    "GB": ["BARC", "LOYD", "NWBK", "HBUK"],
    "US": ["021000021", "021000089", "026009593", "011000138", "322271627", "121000248", "124303120"],
    "VA": ["001", "002"],
    "VG": ["VPVG", "FCIB"],
}

country_data = {
    "AT": {"length": 20, "bank_code_length": 5, "account_length": 11},
    "AZ": {"length": 28, "bank_codes": bank_codes_data["AZ"], "account_length": 20},
    "BH": {"length": 22, "bank_codes": bank_codes_data["BH"], "account_length": 14},
    "BE": {"length": 16, "bank_code_length": 3, "account_length": 7, "check_digits_length": 2},
    "BA": {"length": 20, "bank_code_length": 3, "branch_code_length": 3, "account_length": 8, "check_digits_length": 2},
    "BR": {"length": 29, "bank_codes": bank_codes_data["BR"], "branch_code_length": 5, "account_length": 10, "account_type_length": 1, "owner_type_length": 1},
    "CZ": {"length": 24, "bank_code_length": 4, "prefix_length": 10, "account_length": 6},
    "DK": {"length": 18, "bank_code_length": 4, "account_length": 9, "check_digit_length": 1},
    "DO": {"length": 28, "bank_codes": bank_codes_data["DO"], "account_length": 20},
    "SV": {"length": 28, "bank_codes": bank_codes_data["SV"], "account_length": 20},
    "EE": {"length": 20, "bank_code_length": 2, "branch_code_length": 2, "account_length": 11, "check_digit_length": 1},
    "FO": {"length": 18, "bank_code_length": 4, "account_length": 9, "check_digit_length": 1},
    "FI": {"length": 18, "bank_code_length": 6, "account_length": 7, "check_digit_length": 1},
    "FR": {"length": 27, "bank_code_length": 5, "branch_code_length": 5, "account_length": 11, "key_length": 2},
    "GE": {"length": 22, "bank_codes": bank_codes_data["GE"], "account_length": 16},
    "DE": {"length": 22, "bank_codes": bank_codes_data["DE"], "account_length": 10},
    "GI": {"length": 23, "bank_codes": bank_codes_data["GI"], "account_length": 15},
    "GL": {"length": 18, "bank_code_length": 4, "account_length": 9, "check_digit_length": 1},
    "GT": {"length": 28, "bank_codes": bank_codes_data["GT"], "account_length": 20},
    "HU": {"length": 28, "bank_code_length": 3, "branch_code_length": 4, "check_digit_length": 1, "account_length": 15, "second_check_digit_length": 1},
    "IS": {"length": 26, "bank_code_length": 4, "branch_code_length": 2, "identification_length": 6, "account_length": 10},
    "IE": {"length": 22, "bank_codes": bank_codes_data["IE"], "sort_code_length": 6, "account_length": 8},
    "IT": {"length": 27, "check_char": True, "bank_code_length": 5, "branch_code_length": 5, "account_length": 12},
    "JO": {"length": 30, "bank_codes": bank_codes_data["JO"], "branch_code_length": 4, "account_length": 18},
    "KZ": {"length": 20, "bank_code_length": 3, "account_length": 13},
    "XK": {"length": 20, "bank_code_length": 4, "account_length": 10, "check_digits_length": 2},
    "KW": {"length": 30, "bank_codes": bank_codes_data["KW"], "account_length": 22},
    "LV": {"length": 21, "bank_codes": bank_codes_data["LV"], "account_length": 13},
    "LB": {"length": 28, "bank_code_length": 4, "account_length": 20},
    "LI": {"length": 21, "bank_code_length": 5, "account_length": 12},
    "LT": {"length": 20, "bank_code_length": 5, "account_length": 11},
    "LU": {"length": 20, "bank_code_length": 3, "account_length": 13},
    "MK": {"length": 19, "bank_code_length": 3, "account_length": 10, "check_digits_length": 2},
    "MT": {"length": 31, "bank_codes": bank_codes_data["MT"], "branch_code_length": 5, "account_length": 18},
    "MR": {"length": 27, "bank_code_length": 5, "branch_code_length": 5, "account_length": 11, "check_digits_length": 2},
    "MC": {"length": 27, "bank_code_length": 5, "branch_code_length": 5, "account_length": 11, "key_length": 2},
    "ME": {"length": 22, "bank_code_length": 3, "account_length": 13, "check_digits_length": 2},
    "NO": {"length": 15, "bank_code_length": 4, "account_length": 6, "check_digit_length": 1},
    "PK": {"length": 24, "bank_codes": bank_codes_data["PK"], "account_length": 16},
    "PL": {"length": 28, "bank_codes": bank_codes_data["PL"], "account_length": 16},
    "QA": {"length": 29, "bank_codes": bank_codes_data["QA"], "account_length": 21},
    "MD": {"length": 24, "bank_codes": bank_codes_data["MD"], "account_length": 18},
    "RO": {"length": 24, "bank_codes": bank_codes_data["RO"], "account_length": 16},
    "SM": {"length": 27, "check_char": True, "bank_code_length": 5, "branch_code_length": 5, "account_length": 12},
    "SA": {"length": 24, "bank_code_length": 2, "account_length": 18},
    "RS": {"length": 22, "bank_code_length": 3, "account_length": 13, "check_digits_length": 2},
    "SK": {"length": 24, "bank_code_length": 4, "prefix_length": 6, "account_length": 10},
    "ES": {"length": 24, "bank_code_length": 4, "branch_code_length": 4, "check_digits_length": 2, "account_length": 10},
    "CH": {"length": 21, "bank_code_length": 5, "account_length": 12},
    "TH": {"length": 22, "bank_codes": bank_codes_data["TH"], "branch_code_length": 4, "account_length": 11},
    "TR": {"length": 26, "bank_code_length": 5, "reserved_length": 1, "account_length": 16},
    "UA": {"length": 29, "bank_code_length": 6, "account_length": 19},
    "AE": {"length": 23, "bank_code_length": 3, "account_length": 16},
    "GB": {"length": 22, "bank_codes": bank_codes_data["GB"], "sort_code_length": 6, "account_length": 8},
    "US": {"length": 26, "bank_codes": bank_codes_data["US"], "account_length": 13},
    "VA": {"length": 22, "bank_code_length": 3, "account_length": 15},
    "VG": {"length": 24, "bank_codes": bank_codes_data["VG"], "account_length": 16},
}


def letter_to_number(c: str) -> str:
    """Convert a letter to its IBAN numeric equivalent (A=10, B=11, …, Z=35).

    Digits are returned unchanged.

    Args:
        c: A single character (letter or digit).

    Returns:
        String representation of the numeric value.
    """
    return str(ord(c.upper()) - 55) if c.isalpha() else c


def generate_numeric(length: int) -> str:
    """Generate a random numeric string of the given length.

    Args:
        length: Number of digits to generate.

    Returns:
        A string of random decimal digits.
    """
    return "".join(str(random.randint(0, 9)) for _ in range(length))


def generate_alpha(length: int) -> str:
    """Generate a random uppercase alphabetic string of the given length.

    Args:
        length: Number of characters to generate.

    Returns:
        A string of random uppercase ASCII letters.
    """
    return "".join(random.choice(string.ascii_uppercase) for _ in range(length))


def generate_alphanum(length: int) -> str:
    """Generate a random alphanumeric string (uppercase letters + digits).

    Args:
        length: Number of characters to generate.

    Returns:
        A string of random uppercase letters and digits.
    """
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def calculate_check_digits(country: str, bban: str) -> str:
    """Compute the two-digit IBAN check digits using MOD-97 arithmetic.

    Args:
        country: ISO 3166-1 alpha-2 country code (e.g. ``"DE"``).
        bban: The Basic Bank Account Number portion of the IBAN.

    Returns:
        Two-character string of check digits (zero-padded, e.g. ``"04"``).
    """
    temp_iban = bban + country + "00"
    numeric_str = "".join(letter_to_number(c) for c in temp_iban)
    mod = 0
    for i in range(0, len(numeric_str), 9):
        chunk = numeric_str[i : i + 9]
        mod = (mod * (10 ** len(chunk)) + int(chunk)) % 97
    check_digits = 98 - mod
    return f"{check_digits:02d}"


def validate_iban(iban: str) -> bool:
    """Validate an IBAN using the MOD-97 check algorithm.

    Args:
        iban: The full IBAN string to validate.

    Returns:
        ``True`` if the IBAN is structurally valid, ``False`` otherwise.
    """
    if not iban or len(iban) < 4:
        return False
    country = iban[:2]
    if country not in COUNTRY_GENERATORS:
        return False
    temp_iban = iban[4:] + iban[:4]
    numeric_str = "".join(letter_to_number(c) for c in temp_iban)
    mod = 0
    for i in range(0, len(numeric_str), 9):
        chunk = numeric_str[i : i + 9]
        mod = (mod * (10 ** len(chunk)) + int(chunk)) % 97
    return mod == 1


def generate_at():
    """Generate Austrian (AT) BBAN."""
    data = country_data["AT"]
    bank_code = random.choice(bank_codes_data["AT"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number


def generate_az():
    """Generate Azerbaijani (AZ) BBAN."""
    data = country_data["AZ"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_bh():
    """Generate Bahraini (BH) BBAN."""
    data = country_data["BH"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_be():
    """Generate Belgian (BE) BBAN with mod-97 check digits."""
    data = country_data["BE"]
    bank_code = random.choice(bank_codes_data["BE"])
    account_number = generate_numeric(data["account_length"])
    base = bank_code + account_number
    check_digits = f"{97 - (int(base) % 97):02d}"
    return bank_code + account_number + check_digits


def generate_ba():
    """Generate Bosnian (BA) BBAN."""
    data = country_data["BA"]
    bank_code = random.choice(bank_codes_data["BA"])
    branch_code = generate_numeric(data["branch_code_length"])
    account_number = generate_numeric(data["account_length"])
    check_digits = generate_numeric(data["check_digits_length"])
    return bank_code + branch_code + account_number + check_digits


def generate_br():
    """Generate Brazilian (BR) BBAN."""
    data = country_data["BR"]
    bank_code = random.choice(data["bank_codes"])
    branch_code = generate_numeric(data["branch_code_length"])
    account_number = generate_numeric(data["account_length"])
    account_type = generate_alpha(data["account_type_length"])
    owner_type = generate_alpha(data["owner_type_length"])
    return bank_code + branch_code + account_number + account_type + owner_type


def generate_cz():
    """Generate Czech (CZ) BBAN."""
    data = country_data["CZ"]
    bank_code = random.choice(bank_codes_data["CZ"])
    prefix = generate_numeric(data["prefix_length"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + prefix + account_number


def generate_dk():
    """Generate Danish (DK) BBAN."""
    data = country_data["DK"]
    bank_code = random.choice(bank_codes_data["DK"])
    account_number = generate_numeric(data["account_length"])
    check_digit = generate_numeric(data["check_digit_length"])
    return bank_code + account_number + check_digit


def generate_do():
    """Generate Dominican Republic (DO) BBAN."""
    data = country_data["DO"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number


def generate_sv():
    """Generate Salvadoran (SV) BBAN."""
    data = country_data["SV"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number


def generate_ee():
    """Generate Estonian (EE) BBAN."""
    data = country_data["EE"]
    bank_code = random.choice(bank_codes_data["EE"])
    branch_code = generate_numeric(data["branch_code_length"])
    account_number = generate_numeric(data["account_length"])
    check_digit = generate_numeric(data["check_digit_length"])
    return bank_code + branch_code + account_number + check_digit


def generate_fo():
    """Generate Faroese (FO) BBAN."""
    data = country_data["FO"]
    bank_code = random.choice(bank_codes_data["FO"])
    account_number = generate_numeric(data["account_length"])
    check_digit = generate_numeric(data["check_digit_length"])
    return bank_code + account_number + check_digit


def generate_fi():
    """Generate Finnish (FI) BBAN."""
    data = country_data["FI"]
    bank_code = random.choice(bank_codes_data["FI"])
    account_number = generate_numeric(data["account_length"])
    check_digit = generate_numeric(data["check_digit_length"])
    return bank_code + account_number + check_digit


def generate_fr():
    """Generate French (FR) BBAN."""
    data = country_data["FR"]
    bank_code = random.choice(bank_codes_data["FR"])
    branch_code = generate_numeric(data["branch_code_length"])
    account_number = generate_alphanum(data["account_length"])
    key = generate_numeric(data["key_length"])
    return bank_code + branch_code + account_number + key


def generate_ge():
    """Generate Georgian (GE) BBAN."""
    data = country_data["GE"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number


def generate_de():
    """Generate German (DE) BBAN."""
    data = country_data["DE"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number


def generate_gi():
    """Generate Gibraltarian (GI) BBAN."""
    data = country_data["GI"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_gl():
    """Generate Greenlandic (GL) BBAN."""
    data = country_data["GL"]
    bank_code = random.choice(bank_codes_data["GL"])
    account_number = generate_numeric(data["account_length"])
    check_digit = generate_numeric(data["check_digit_length"])
    return bank_code + account_number + check_digit


def generate_gt():
    """Generate Guatemalan (GT) BBAN."""
    data = country_data["GT"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_hu():
    """Generate Hungarian (HU) BBAN."""
    data = country_data["HU"]
    bank_code = random.choice(bank_codes_data["HU"])
    branch_code = generate_numeric(data["branch_code_length"])
    check_digit = generate_numeric(data["check_digit_length"])
    account_number = generate_numeric(data["account_length"])
    second_check_digit = generate_numeric(data["second_check_digit_length"])
    return bank_code + branch_code + check_digit + account_number + second_check_digit


def generate_is():
    """Generate Icelandic (IS) BBAN."""
    data = country_data["IS"]
    bank_code = random.choice(bank_codes_data["IS"])
    branch_code = generate_numeric(data["branch_code_length"])
    identification = generate_numeric(data["identification_length"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + branch_code + identification + account_number


def generate_ie():
    """Generate Irish (IE) BBAN."""
    data = country_data["IE"]
    bank_code = random.choice(data["bank_codes"])
    sort_code = generate_numeric(data["sort_code_length"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + sort_code + account_number


def generate_it():
    """Generate Italian (IT) BBAN with CIN check character."""
    data = country_data["IT"]
    bank_code = random.choice(bank_codes_data["IT"])
    branch_code = generate_numeric(data["branch_code_length"])
    account_number = generate_alphanum(data["account_length"])
    weights = [1, 0, 5, 7, 9, 13, 15, 17, 19, 21, 2, 4, 18, 20, 11, 3, 6, 8, 12, 14, 16, 10, 22, 25, 24, 23]
    cin_input = bank_code + branch_code + account_number
    total = sum(
        (ord(c) - ord("0") if c.isdigit() else ord(c) - ord("A") + 10) * weights[i % 26]
        for i, c in enumerate(cin_input)
    )
    cin = chr(65 + (total % 26))
    return cin + bank_code + branch_code + account_number


def generate_jo():
    """Generate Jordanian (JO) BBAN."""
    data = country_data["JO"]
    bank_code = random.choice(data["bank_codes"])
    branch_code = generate_numeric(data["branch_code_length"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + branch_code + account_number


def generate_kz():
    """Generate Kazakhstani (KZ) BBAN."""
    data = country_data["KZ"]
    bank_code = random.choice(bank_codes_data["KZ"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_xk():
    """Generate Kosovan (XK) BBAN."""
    data = country_data["XK"]
    bank_code = random.choice(bank_codes_data["XK"])
    account_number = generate_numeric(data["account_length"])
    check_digits = generate_numeric(data["check_digits_length"])
    return bank_code + account_number + check_digits


def generate_kw():
    """Generate Kuwaiti (KW) BBAN."""
    data = country_data["KW"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_lv():
    """Generate Latvian (LV) BBAN."""
    data = country_data["LV"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_lb():
    """Generate Lebanese (LB) BBAN."""
    data = country_data["LB"]
    bank_code = random.choice(bank_codes_data["LB"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_li():
    """Generate Liechtensteiner (LI) BBAN."""
    data = country_data["LI"]
    bank_code = random.choice(bank_codes_data["LI"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_lt():
    """Generate Lithuanian (LT) BBAN."""
    data = country_data["LT"]
    bank_code = random.choice(bank_codes_data["LT"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number


def generate_lu():
    """Generate Luxembourgish (LU) BBAN."""
    data = country_data["LU"]
    bank_code = random.choice(bank_codes_data["LU"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_mk():
    """Generate Macedonian (MK) BBAN."""
    data = country_data["MK"]
    bank_code = random.choice(bank_codes_data["MK"])
    account_number = generate_alphanum(data["account_length"])
    check_digits = generate_numeric(data["check_digits_length"])
    return bank_code + account_number + check_digits


def generate_mt():
    """Generate Maltese (MT) BBAN."""
    data = country_data["MT"]
    bank_code = random.choice(data["bank_codes"])
    branch_code = generate_numeric(data["branch_code_length"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + branch_code + account_number


def generate_mr():
    """Generate Mauritanian (MR) BBAN."""
    data = country_data["MR"]
    bank_code = random.choice(bank_codes_data["MR"])
    branch_code = generate_numeric(data["branch_code_length"])
    account_number = generate_numeric(data["account_length"])
    check_digits = generate_numeric(data["check_digits_length"])
    return bank_code + branch_code + account_number + check_digits


def generate_mc():
    """Generate Monegasque (MC) BBAN."""
    data = country_data["MC"]
    bank_code = random.choice(bank_codes_data["MC"])
    branch_code = generate_numeric(data["branch_code_length"])
    account_number = generate_alphanum(data["account_length"])
    key = generate_numeric(data["key_length"])
    return bank_code + branch_code + account_number + key


def generate_me():
    """Generate Montenegrin (ME) BBAN."""
    data = country_data["ME"]
    bank_code = random.choice(bank_codes_data["ME"])
    account_number = generate_numeric(data["account_length"])
    check_digits = generate_numeric(data["check_digits_length"])
    return bank_code + account_number + check_digits


def generate_no():
    """Generate Norwegian (NO) BBAN with mod-11 check digit."""
    data = country_data["NO"]
    bank_code = random.choice(bank_codes_data["NO"])
    account_number = generate_numeric(data["account_length"])
    base = bank_code + account_number
    weights = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(base[i]) * weights[i] for i in range(len(base)))
    check_digit = (11 - (total % 11)) % 11
    if check_digit == 10:
        check_digit = 0
    return bank_code + account_number + str(check_digit)


def generate_pk():
    """Generate Pakistani (PK) BBAN."""
    data = country_data["PK"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number


def generate_pl():
    """Generate Polish (PL) BBAN."""
    data = country_data["PL"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number


def generate_qa():
    """Generate Qatari (QA) BBAN."""
    data = country_data["QA"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_md():
    """Generate Moldovan (MD) BBAN."""
    data = country_data["MD"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_ro():
    """Generate Romanian (RO) BBAN."""
    data = country_data["RO"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_sm():
    """Generate San Marinese (SM) BBAN with CIN check character."""
    data = country_data["SM"]
    bank_code = random.choice(bank_codes_data["SM"])
    branch_code = generate_numeric(data["branch_code_length"])
    account_number = generate_alphanum(data["account_length"])
    weights = [1, 0, 5, 7, 9, 13, 15, 17, 19, 21, 2, 4, 18, 20, 11, 3, 6, 8, 12, 14, 16, 10, 22, 25, 24, 23]
    cin_input = bank_code + branch_code + account_number
    total = sum(
        (ord(c) - ord("0") if c.isdigit() else ord(c) - ord("A") + 10) * weights[i % 26]
        for i, c in enumerate(cin_input)
    )
    cin = chr(65 + (total % 26))
    return cin + bank_code + branch_code + account_number


def generate_sa():
    """Generate Saudi Arabian (SA) BBAN."""
    data = country_data["SA"]
    bank_code = random.choice(bank_codes_data["SA"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_rs():
    """Generate Serbian (RS) BBAN."""
    data = country_data["RS"]
    bank_code = random.choice(bank_codes_data["RS"])
    account_number = generate_numeric(data["account_length"])
    check_digits = generate_numeric(data["check_digits_length"])
    return bank_code + account_number + check_digits


def generate_sk():
    """Generate Slovak (SK) BBAN."""
    data = country_data["SK"]
    bank_code = random.choice(bank_codes_data["SK"])
    prefix = generate_numeric(data["prefix_length"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + prefix + account_number


def generate_es():
    """Generate Spanish (ES) BBAN with double mod-11 check digits."""
    data = country_data["ES"]
    bank_code = random.choice(bank_codes_data["ES"])
    branch_code = generate_numeric(data["branch_code_length"])
    account_number = generate_numeric(data["account_length"])
    base = bank_code + branch_code
    weights = [4, 8, 5, 10, 9, 7, 3, 6]
    total = sum(int(base[i]) * weights[i] for i in range(len(base)))
    check_digit1 = (11 - (total % 11)) % 11
    if check_digit1 == 10:
        check_digit1 = 1
    elif check_digit1 == 11:
        check_digit1 = 0
    weights2 = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]
    total2 = sum(int(account_number[i]) * weights2[i] for i in range(len(account_number)))
    check_digit2 = (11 - (total2 % 11)) % 11
    if check_digit2 == 10:
        check_digit2 = 1
    elif check_digit2 == 11:
        check_digit2 = 0
    return bank_code + branch_code + f"{check_digit1}{check_digit2}" + account_number


def generate_ch():
    """Generate Swiss (CH) BBAN."""
    data = country_data["CH"]
    bank_code = random.choice(bank_codes_data["CH"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_th():
    """Generate Thai (TH) BBAN."""
    data = country_data["TH"]
    bank_code = random.choice(data["bank_codes"])
    branch_code = generate_numeric(data["branch_code_length"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + branch_code + account_number


def generate_tr():
    """Generate Turkish (TR) BBAN."""
    data = country_data["TR"]
    bank_code = random.choice(bank_codes_data["TR"])
    reserved = generate_numeric(data["reserved_length"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + reserved + account_number


def generate_ua():
    """Generate Ukrainian (UA) BBAN."""
    data = country_data["UA"]
    bank_code = random.choice(bank_codes_data["UA"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number


def generate_ae():
    """Generate UAE (AE) BBAN."""
    data = country_data["AE"]
    bank_code = random.choice(bank_codes_data["AE"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number


def generate_gb():
    """Generate British (GB) BBAN."""
    data = country_data["GB"]
    bank_code = random.choice(data["bank_codes"])
    sort_code = generate_numeric(data["sort_code_length"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + sort_code + account_number


def generate_us():
    """Generate US BBAN (non-standard, for testing purposes)."""
    data = country_data["US"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number


def generate_va():
    """Generate Vatican (VA) BBAN."""
    data = country_data["VA"]
    bank_code = random.choice(bank_codes_data["VA"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number


def generate_vg():
    """Generate British Virgin Islands (VG) BBAN."""
    data = country_data["VG"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number


COUNTRY_GENERATORS = {
    "AT": {"length": 20, "generator": generate_at},
    "AZ": {"length": 28, "generator": generate_az},
    "BH": {"length": 22, "generator": generate_bh},
    "BE": {"length": 16, "generator": generate_be},
    "BA": {"length": 20, "generator": generate_ba},
    "BR": {"length": 29, "generator": generate_br},
    "CZ": {"length": 24, "generator": generate_cz},
    "DK": {"length": 18, "generator": generate_dk},
    "DO": {"length": 28, "generator": generate_do},
    "SV": {"length": 28, "generator": generate_sv},
    "EE": {"length": 20, "generator": generate_ee},
    "FO": {"length": 18, "generator": generate_fo},
    "FI": {"length": 18, "generator": generate_fi},
    "FR": {"length": 27, "generator": generate_fr},
    "GE": {"length": 22, "generator": generate_ge},
    "DE": {"length": 22, "generator": generate_de},
    "GI": {"length": 23, "generator": generate_gi},
    "GL": {"length": 18, "generator": generate_gl},
    "GT": {"length": 28, "generator": generate_gt},
    "HU": {"length": 28, "generator": generate_hu},
    "IS": {"length": 26, "generator": generate_is},
    "IE": {"length": 22, "generator": generate_ie},
    "IT": {"length": 27, "generator": generate_it},
    "JO": {"length": 30, "generator": generate_jo},
    "KZ": {"length": 20, "generator": generate_kz},
    "XK": {"length": 20, "generator": generate_xk},
    "KW": {"length": 30, "generator": generate_kw},
    "LV": {"length": 21, "generator": generate_lv},
    "LB": {"length": 28, "generator": generate_lb},
    "LI": {"length": 21, "generator": generate_li},
    "LT": {"length": 20, "generator": generate_lt},
    "LU": {"length": 20, "generator": generate_lu},
    "MK": {"length": 19, "generator": generate_mk},
    "MT": {"length": 31, "generator": generate_mt},
    "MR": {"length": 27, "generator": generate_mr},
    "MC": {"length": 27, "generator": generate_mc},
    "ME": {"length": 22, "generator": generate_me},
    "NO": {"length": 15, "generator": generate_no},
    "PK": {"length": 24, "generator": generate_pk},
    "PL": {"length": 28, "generator": generate_pl},
    "QA": {"length": 29, "generator": generate_qa},
    "MD": {"length": 24, "generator": generate_md},
    "RO": {"length": 24, "generator": generate_ro},
    "SM": {"length": 27, "generator": generate_sm},
    "SA": {"length": 24, "generator": generate_sa},
    "RS": {"length": 22, "generator": generate_rs},
    "SK": {"length": 24, "generator": generate_sk},
    "ES": {"length": 24, "generator": generate_es},
    "CH": {"length": 21, "generator": generate_ch},
    "TH": {"length": 22, "generator": generate_th},
    "TR": {"length": 26, "generator": generate_tr},
    "UA": {"length": 29, "generator": generate_ua},
    "AE": {"length": 23, "generator": generate_ae},
    "GB": {"length": 22, "generator": generate_gb},
    "US": {"length": 26, "generator": generate_us},
    "VA": {"length": 22, "generator": generate_va},
    "VG": {"length": 24, "generator": generate_vg},
}


async def agenerate_numeric(length: int) -> str:
    """Async wrapper around :func:`generate_numeric`."""
    return generate_numeric(length)


async def agenerate_alpha(length: int) -> str:
    """Async wrapper around :func:`generate_alpha`."""
    return generate_alpha(length)


async def agenerate_alphanum(length: int) -> str:
    """Async wrapper around :func:`generate_alphanum`."""
    return generate_alphanum(length)


async def acalculate_check_digits(country: str, bban: str) -> str:
    """Async wrapper around :func:`calculate_check_digits`.

    Defers the (cheap) computation through ``asyncio`` so callers can
    ``await`` it inside coroutines without blocking semantics.
    """
    return calculate_check_digits(country, bban)


async def avalidate_iban(iban: str) -> bool:
    """Async wrapper around :func:`validate_iban`."""
    return validate_iban(iban)

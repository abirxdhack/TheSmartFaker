#Copyright @ISmartCoder
#Updates Channel @TheSmartDev
import random
import string

bank_codes_data = {
    "AT": ["12000", "20151"],
    "AZ": ["NABZ", "AIIB"],
    "BH": ["BBKU", "AUBB"],
    "BE": ["001", "310"],
    "BA": ["129", "199"],
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
    "TR": ["00061", "00134"],
    "UA": ["300346", "300536"],
    "AE": ["033", "040"],
    "GB": ["BARC", "LOYD", "NWBK", "HBUK"],
    "VA": ["001", "002"],
    "VG": ["VPVG", "FCIB"]
}

country_data = {
    "AT": {"length": 20, "bank_code_length": 5, "account_length": 11},
    "AZ": {"length": 28, "bank_codes": bank_codes_data["AZ"], "account_length": 20},
    "BH": {"length": 22, "bank_codes": bank_codes_data["BH"], "account_length": 14},
    "BE": {"length": 16, "bank_code_length": 3, "account_length": 7, "check_digits_length": 2},
    "BA": {"length": 20, "bank_code_length": 3, "branch_code_length": 3, "account_length": 8, "check_digits_length": 2},
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
    "TR": {"length": 26, "bank_code_length": 5, "reserved_length": 1, "account_length": 16},
    "UA": {"length": 29, "bank_code_length": 6, "account_length": 19},
    "AE": {"length": 23, "bank_code_length": 3, "account_length": 16},
    "GB": {"length": 22, "bank_codes": bank_codes_data["GB"], "sort_code_length": 6, "account_length": 8},
    "VA": {"length": 22, "bank_code_length": 3, "account_length": 15},
    "VG": {"length": 24, "bank_codes": bank_codes_data["VG"], "account_length": 16}
}

def letter_to_number(c: str) -> str:
    """Convert a letter to its IBAN numeric equivalent."""
    return str(ord(c.upper()) - 55) if c.isalpha() else c

async def generate_numeric(length: int) -> str:
    """Generate a random numeric string of specified length."""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

async def generate_alpha(length: int) -> str:
    """Generate a random alphabetic string of specified length."""
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

async def generate_alphanum(length: int) -> str:
    """Generate a random alphanumeric string of specified length."""
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

async def calculate_check_digits(country: str, bban: str) -> str:
    """Calculate IBAN check digits using ISO 7064 MOD 97-10."""
    temp_iban = bban + country + "00"
    numeric_str = ''.join(letter_to_number(c) for c in temp_iban)
    mod = 0
    for i in range(0, len(numeric_str), 9):
        chunk = numeric_str[i:i+9]
        mod = (mod * (10 ** len(chunk)) + int(chunk)) % 97
    check_digits = 98 - mod
    return f"{check_digits:02d}"

async def validate_iban(iban: str) -> bool:
    """Validate an IBAN using ISO 7064 MOD 97-10."""
    if not iban or len(iban) < 4:
        return False
    country = iban[:2]
    if country not in COUNTRY_GENERATORS:
        return False
    temp_iban = iban[4:] + iban[:4]
    numeric_str = ''.join(letter_to_number(c) for c in temp_iban)
    mod = 0
    for i in range(0, len(numeric_str), 9):
        chunk = numeric_str[i:i+9]
        mod = (mod * (10 ** len(chunk)) + int(chunk)) % 97
    return mod == 1

async def generate_at():
    """Generate BBAN for Austria."""
    data = country_data["AT"]
    bank_code = random.choice(bank_codes_data["AT"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + account_number

async def generate_az():
    """Generate BBAN for Azerbaijan."""
    data = country_data["AZ"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_bh():
    """Generate BBAN for Bahrain."""
    data = country_data["BH"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_be():
    """Generate BBAN for Belgium."""
    data = country_data["BE"]
    bank_code = random.choice(bank_codes_data["BE"])
    account_number = await generate_numeric(data["account_length"])
    base = bank_code + account_number
    check_digits = f"{97 - (int(base) % 97):02d}"
    return bank_code + account_number + check_digits

async def generate_ba():
    """Generate BBAN for Bosnia and Herzegovina."""
    data = country_data["BA"]
    bank_code = random.choice(bank_codes_data["BA"])
    branch_code = await generate_numeric(data["branch_code_length"])
    account_number = await generate_numeric(data["account_length"])
    check_digits = await generate_numeric(data["check_digits_length"])
    return bank_code + branch_code + account_number + check_digits

async def generate_cz():
    """Generate BBAN for Czech Republic."""
    data = country_data["CZ"]
    bank_code = random.choice(bank_codes_data["CZ"])
    prefix = await generate_numeric(data["prefix_length"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + prefix + account_number

async def generate_dk():
    """Generate BBAN for Denmark."""
    data = country_data["DK"]
    bank_code = random.choice(bank_codes_data["DK"])
    account_number = await generate_numeric(data["account_length"])
    check_digit = await generate_numeric(data["check_digit_length"])
    return bank_code + account_number + check_digit

async def generate_do():
    """Generate BBAN for Dominican Republic."""
    data = country_data["DO"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + account_number

async def generate_sv():
    """Generate BBAN for El Salvador."""
    data = country_data["SV"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + account_number

async def generate_ee():
    """Generate BBAN for Estonia."""
    data = country_data["EE"]
    bank_code = random.choice(bank_codes_data["EE"])
    branch_code = await generate_numeric(data["branch_code_length"])
    account_number = await generate_numeric(data["account_length"])
    check_digit = await generate_numeric(data["check_digit_length"])
    return bank_code + branch_code + account_number + check_digit

async def generate_fo():
    """Generate BBAN for Faroe Islands."""
    data = country_data["FO"]
    bank_code = random.choice(bank_codes_data["FO"])
    account_number = await generate_numeric(data["account_length"])
    check_digit = await generate_numeric(data["check_digit_length"])
    return bank_code + account_number + check_digit

async def generate_fi():
    """Generate BBAN for Finland."""
    data = country_data["FI"]
    bank_code = random.choice(bank_codes_data["FI"])
    account_number = await generate_numeric(data["account_length"])
    check_digit = await generate_numeric(data["check_digit_length"])
    return bank_code + account_number + check_digit

async def generate_fr():
    """Generate BBAN for France."""
    data = country_data["FR"]
    bank_code = random.choice(bank_codes_data["FR"])
    branch_code = await generate_numeric(data["branch_code_length"])
    account_number = await generate_alphanum(data["account_length"])
    key = await generate_numeric(data["key_length"])
    return bank_code + branch_code + account_number + key

async def generate_ge():
    """Generate BBAN for Georgia."""
    data = country_data["GE"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + account_number

async def generate_de():
    """Generate BBAN for Germany."""
    data = country_data["DE"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + account_number

async def generate_gi():
    """Generate BBAN for Gibraltar."""
    data = country_data["GI"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_gl():
    """Generate BBAN for Greenland."""
    data = country_data["GL"]
    bank_code = random.choice(bank_codes_data["GL"])
    account_number = await generate_numeric(data["account_length"])
    check_digit = await generate_numeric(data["check_digit_length"])
    return bank_code + account_number + check_digit

async def generate_gt():
    """Generate BBAN for Guatemala."""
    data = country_data["GT"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_hu():
    """Generate BBAN for Hungary."""
    data = country_data["HU"]
    bank_code = random.choice(bank_codes_data["HU"])
    branch_code = await generate_numeric(data["branch_code_length"])
    check_digit = await generate_numeric(data["check_digit_length"])
    account_number = await generate_numeric(data["account_length"])
    second_check_digit = await generate_numeric(data["second_check_digit_length"])
    return bank_code + branch_code + check_digit + account_number + second_check_digit

async def generate_is():
    """Generate BBAN for Iceland."""
    data = country_data["IS"]
    bank_code = random.choice(bank_codes_data["IS"])
    branch_code = await generate_numeric(data["branch_code_length"])
    identification = await generate_numeric(data["identification_length"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + branch_code + identification + account_number

async def generate_ie():
    """Generate BBAN for Ireland."""
    data = country_data["IE"]
    bank_code = random.choice(data["bank_codes"])
    sort_code = await generate_numeric(data["sort_code_length"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + sort_code + account_number

async def generate_it():
    """Generate BBAN for Italy."""
    data = country_data["IT"]
    bank_code = random.choice(bank_codes_data["IT"])
    branch_code = await generate_numeric(data["branch_code_length"])
    account_number = await generate_alphanum(data["account_length"])
    weights = [1, 0, 5, 7, 9, 13, 15, 17, 19, 21, 2, 4, 18, 20, 11, 3, 6, 8, 12, 14, 16, 10, 22, 25, 24, 23]
    cin_input = bank_code + branch_code + account_number
    total = sum((ord(c) - ord('0') if c.isdigit() else ord(c) - ord('A') + 10) * weights[i % 26] for i, c in enumerate(cin_input))
    cin = chr(65 + (total % 26))
    return cin + bank_code + branch_code + account_number

async def generate_jo():
    """Generate BBAN for Jordan."""
    data = country_data["JO"]
    bank_code = random.choice(data["bank_codes"])
    branch_code = await generate_numeric(data["branch_code_length"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + branch_code + account_number

async def generate_kz():
    """Generate BBAN for Kazakhstan."""
    data = country_data["KZ"]
    bank_code = random.choice(bank_codes_data["KZ"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_xk():
    """Generate BBAN for Kosovo."""
    data = country_data["XK"]
    bank_code = random.choice(bank_codes_data["XK"])
    account_number = await generate_numeric(data["account_length"])
    check_digits = await generate_numeric(data["check_digits_length"])
    return bank_code + account_number + check_digits

async def generate_kw():
    """Generate BBAN for Kuwait."""
    data = country_data["KW"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_lv():
    """Generate BBAN for Latvia."""
    data = country_data["LV"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_lb():
    """Generate BBAN for Lebanon."""
    data = country_data["LB"]
    bank_code = random.choice(bank_codes_data["LB"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_li():
    """Generate BBAN for Liechtenstein."""
    data = country_data["LI"]
    bank_code = random.choice(bank_codes_data["LI"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_lt():
    """Generate BBAN for Lithuania."""
    data = country_data["LT"]
    bank_code = random.choice(bank_codes_data["LT"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + account_number

async def generate_lu():
    """Generate BBAN for Luxembourg."""
    data = country_data["LU"]
    bank_code = random.choice(bank_codes_data["LU"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_mk():
    """Generate BBAN for North Macedonia."""
    data = country_data["MK"]
    bank_code = random.choice(bank_codes_data["MK"])
    account_number = await generate_alphanum(data["account_length"])
    check_digits = await generate_numeric(data["check_digits_length"])
    return bank_code + account_number + check_digits

async def generate_mt():
    """Generate BBAN for Malta."""
    data = country_data["MT"]
    bank_code = random.choice(data["bank_codes"])
    branch_code = await generate_numeric(data["branch_code_length"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + branch_code + account_number

async def generate_mr():
    """Generate BBAN for Mauritania."""
    data = country_data["MR"]
    bank_code = random.choice(bank_codes_data["MR"])
    branch_code = await generate_numeric(data["branch_code_length"])
    account_number = await generate_numeric(data["account_length"])
    check_digits = await generate_numeric(data["check_digits_length"])
    return bank_code + branch_code + account_number + check_digits

async def generate_mc():
    """Generate BBAN for Monaco."""
    data = country_data["MC"]
    bank_code = random.choice(bank_codes_data["MC"])
    branch_code = await generate_numeric(data["branch_code_length"])
    account_number = await generate_alphanum(data["account_length"])
    key = await generate_numeric(data["key_length"])
    return bank_code + branch_code + account_number + key

async def generate_me():
    """Generate BBAN for Montenegro."""
    data = country_data["ME"]
    bank_code = random.choice(bank_codes_data["ME"])
    account_number = await generate_numeric(data["account_length"])
    check_digits = await generate_numeric(data["check_digits_length"])
    return bank_code + account_number + check_digits

async def generate_no():
    """Generate BBAN for Norway."""
    data = country_data["NO"]
    bank_code = random.choice(bank_codes_data["NO"])
    account_number = await generate_numeric(data["account_length"])
    base = bank_code + account_number
    weights = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(base[i]) * weights[i] for i in range(len(base)))
    check_digit = (11 - (total % 11)) % 11
    if check_digit == 10:
        check_digit = 0
    return bank_code + account_number + str(check_digit)

async def generate_pk():
    """Generate BBAN for Pakistan."""
    data = country_data["PK"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + account_number

async def generate_pl():
    """Generate BBAN for Poland."""
    data = country_data["PL"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + account_number

async def generate_qa():
    """Generate BBAN for Qatar."""
    data = country_data["QA"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_md():
    """Generate BBAN for Moldova."""
    data = country_data["MD"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_ro():
    """Generate BBAN for Romania."""
    data = country_data["RO"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_sm():
    """Generate BBAN for San Marino."""
    data = country_data["SM"]
    bank_code = random.choice(bank_codes_data["SM"])
    branch_code = await generate_numeric(data["branch_code_length"])
    account_number = await generate_alphanum(data["account_length"])
    weights = [1, 0, 5, 7, 9, 13, 15, 17, 19, 21, 2, 4, 18, 20, 11, 3, 6, 8, 12, 14, 16, 10, 22, 25, 24, 23]
    cin_input = bank_code + branch_code + account_number
    total = sum((ord(c) - ord('0') if c.isdigit() else ord(c) - ord('A') + 10) * weights[i % 26] for i, c in enumerate(cin_input))
    cin = chr(65 + (total % 26))
    return cin + bank_code + branch_code + account_number

async def generate_sa():
    """Generate BBAN for Saudi Arabia."""
    data = country_data["SA"]
    bank_code = random.choice(bank_codes_data["SA"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_rs():
    """Generate BBAN for Serbia."""
    data = country_data["RS"]
    bank_code = random.choice(bank_codes_data["RS"])
    account_number = await generate_numeric(data["account_length"])
    check_digits = await generate_numeric(data["check_digits_length"])
    return bank_code + account_number + check_digits

async def generate_sk():
    """Generate BBAN for Slovakia."""
    data = country_data["SK"]
    bank_code = random.choice(bank_codes_data["SK"])
    prefix = await generate_numeric(data["prefix_length"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + prefix + account_number

async def generate_es():
    """Generate BBAN for Spain."""
    data = country_data["ES"]
    bank_code = random.choice(bank_codes_data["ES"])
    branch_code = await generate_numeric(data["branch_code_length"])
    account_number = await generate_numeric(data["account_length"])
    base = bank_code + branch_code
    weights = [4, 8, 5, 10, 9, 7, 3, 6]
    total = sum(int(base[i]) * weights[i] for i in range(len(base)))
    check_digit1 = (11 - (total % 11)) % 11
    if check_digit1 == 10:
        check_digit1 = 1
    elif check_digit1 == 11:
        check_digit1 = 0
    base = account_number
    weights = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]
    total = sum(int(base[i]) * weights[i] for i in range(len(base)))
    check_digit2 = (11 - (total % 11)) % 11
    if check_digit2 == 10:
        check_digit2 = 1
    elif check_digit2 == 11:
        check_digit2 = 0
    check_digits = f"{check_digit1}{check_digit2}"
    return bank_code + branch_code + check_digits + account_number

async def generate_ch():
    """Generate BBAN for Switzerland."""
    data = country_data["CH"]
    bank_code = random.choice(bank_codes_data["CH"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_tr():
    """Generate BBAN for Turkey."""
    data = country_data["TR"]
    bank_code = random.choice(bank_codes_data["TR"])
    reserved = await generate_numeric(data["reserved_length"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + reserved + account_number

async def generate_ua():
    """Generate BBAN for Ukraine."""
    data = country_data["UA"]
    bank_code = random.choice(bank_codes_data["UA"])
    account_number = await generate_alphanum(data["account_length"])
    return bank_code + account_number

async def generate_ae():
    """Generate BBAN for United Arab Emirates."""
    data = country_data["AE"]
    bank_code = random.choice(bank_codes_data["AE"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + account_number

async def generate_gb():
    """Generate BBAN for United Kingdom."""
    data = country_data["GB"]
    bank_code = random.choice(data["bank_codes"])
    sort_code = await generate_numeric(data["sort_code_length"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + sort_code + account_number

async def generate_va():
    """Generate BBAN for Vatican City."""
    data = country_data["VA"]
    bank_code = random.choice(bank_codes_data["VA"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + account_number

async def generate_vg():
    """Generate BBAN for British Virgin Islands."""
    data = country_data["VG"]
    bank_code = random.choice(data["bank_codes"])
    account_number = await generate_numeric(data["account_length"])
    return bank_code + account_number

COUNTRY_GENERATORS = {
    "AT": {"length": 20, "generator": generate_at},
    "AZ": {"length": 28, "generator": generate_az},
    "BH": {"length": 22, "generator": generate_bh},
    "BE": {"length": 16, "generator": generate_be},
    "BA": {"length": 20, "generator": generate_ba},
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
    "TR": {"length": 26, "generator": generate_tr},
    "UA": {"length": 29, "generator": generate_ua},
    "AE": {"length": 23, "generator": generate_ae},
    "GB": {"length": 22, "generator": generate_gb},
    "VA": {"length": 22, "generator": generate_va},
    "VG": {"length": 24, "generator": generate_vg}
}

def generate_unicode_range(start, end):
    return [chr(i) for i in range(start, end)]

latin1_supplement_digits = (0x0030, 0x003a)
fullwidth_digits = (0xFF10, 0xFF1A)
mathematical_bold_digits = (0x1D7CE, 0x1D7D8)
mathematical_double_struck_digits = (0x1D7D8, 0x1D7E2)
mathematical_sans_serif_digits = (0x1D7E2, 0x1D7EC)
mathematical_sans_serif_bold_digits = (0x1D7EC, 0x1D7F6)
mathematical_monospace_digits = (0x1D7F6, 0x1D800)
circled_digits = (0x2460, 0x246A)
dingbat_negative_circled_digits = (0x2775, 0x2780)
dingbats = (0x2780, 0x2789)
enclosed_digits = (0x24B6, 0x24BF)
subscript_digits = (0x2080, 0x208A)
superscript_digits = (0x2070, 0x207A)

categories = {
    "Latin1 Supplement Digits": latin1_supplement_digits,
    "Fullwidth Digits": fullwidth_digits,
    "Mathematical Bold Digits": mathematical_bold_digits,
    "Mathematical Double-Struck Digits": mathematical_double_struck_digits,
    "Mathematical Sans-Serif Digits": mathematical_sans_serif_digits,
    "Mathematical Sans-Serif Bold Digits": mathematical_sans_serif_bold_digits,
    "Mathematical Monospace Digits": mathematical_monospace_digits,
    "Circled Digits": circled_digits,
    "Dingbat Negative Circled Digits": dingbat_negative_circled_digits,
    "Dingbats": (0x1F10B,) + dingbats,
    "Enclosed Digits": enclosed_digits,
    "Subscript Digits": subscript_digits,
    "Superscript Digits": superscript_digits,
}

for category, range_values in categories.items():
    if isinstance(range_values, tuple):
        print(f"{category}: {generate_unicode_range(*range_values)}")
    else:
        print(f"{category}: {[chr(range_values[0])] + generate_unicode_range(*range_values[1:])}")

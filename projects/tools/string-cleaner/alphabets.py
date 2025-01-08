def generate_unicode_range(start, end):
    return [chr(i) for i in range(start, end)]

# Mathematical Bold Uppercase Letters
mathematical_bold_uppercase = (0x1D400, 0x1D41A)

# Mathematical Bold Lowercase Letters
mathematical_bold_lowercase = (0x1D41A, 0x1D434)

# Mathematical Italic Uppercase Letters
mathematical_italic_uppercase = (0x1D434, 0x1D44E)

# Mathematical Italic Lowercase Letters
mathematical_italic_lowercase = (0x1D44e, 0x1D468)

# Mathematical Bold Italic Uppercase Letters
mathematical_bold_italic_uppercase = (0x1D468, 0x1D482)

# Mathematical Bold Italic Lowercase Letters
mathematical_bold_italic_lowercase = (0x1D482, 0x1D49C)

# Mathematical Script Uppercase Letters
mathematical_script_uppercase = (0x1D49C, 0x1D4B6)

# Mathematical Script Lowercase Letters
mathematical_script_lowercase = (0x1D4B6, 0x1D4D0)

# ---

# Mathematical Bold Script Uppercase Letters
mathematical_bold_script_uppercase = (0x1D4D0, 0x1D4EA)

# Mathematical Bold Script Lowercase Letters
mathematical_bold_script_lowercase = (0x1D4EB, 0x1D505)

# Mathematical Fraktur Uppercase Letters
mathematical_fraktur_uppercase = (0x1D504, 0x1D51E)

# Mathematical Fraktur Lowercase Letters
mathematical_fraktur_lowercase = (0x1D51F, 0x1D539)

# Mathematical Double-Struck Uppercase Letters
mathematical_double_struck_uppercase = (0x1D538, 0x1D552)

# Mathematical Double-Struck Lowercase Letters
mathematical_double_struck_lowercase = (0x1D553, 0x1D56D)

# Sans-Serif Bold Uppercase Letters
sans_serif_bold_uppercase = (0x1D5A0, 0x1D5BA)

# Sans-Serif Bold Lowercase Letters
sans_serif_bold_lowercase = (0x1D5BB, 0x1D5D5)

# Sans-Serif Italic Uppercase Letters
sans_serif_italic_uppercase = (0x1D608, 0x1D622)

# Sans-Serif Italic Lowercase Letters
sans_serif_italic_lowercase = (0x1D623, 0x1D63D)

# Sans-Serif Bold Italic Uppercase Letters
sans_serif_bold_italic_uppercase = (0x1D63C, 0x1D656)

# Sans-Serif Bold Italic Lowercase Letters
sans_serif_bold_italic_lowercase = (0x1D657, 0x1D671)

# Monospace Uppercase Letters
monospace_uppercase = (0x1D670, 0x1D68A)

# Monospace Lowercase Letters
monospace_lowercase = (0x1D68B, 0x1D6A5)

categories = {
    "Mathematical Bold Uppercase Letters": mathematical_bold_uppercase,
    "Mathematical Bold Lowercase Letters": mathematical_bold_lowercase,
    "Mathematical Italic Uppercase Letters": mathematical_italic_uppercase,
    "Mathematical Italic Lowercase Letters": mathematical_italic_lowercase,
    "Mathematical Bold Italic Uppercase Letters": mathematical_bold_italic_uppercase,
    "Mathematical Bold Italic Lowercase Letters": mathematical_bold_italic_lowercase,
    "Mathematical Script Uppercase Letters": mathematical_script_uppercase,
    "Mathematical Script Lowercase Letters": mathematical_script_lowercase,
    "Mathematical Bold Script Uppercase Letters": mathematical_bold_script_uppercase,
    "Mathematical Bold Script Lowercase Letters": mathematical_bold_script_lowercase,
    "Mathematical Fraktur Uppercase Letters": mathematical_fraktur_uppercase,
    "Mathematical Fraktur Lowercase Letters": mathematical_fraktur_lowercase,
    "Mathematical Double-Struck Uppercase Letters": mathematical_double_struck_uppercase,
    "Mathematical Double-Struck Lowercase Letters": mathematical_double_struck_lowercase,
    "Sans-Serif Bold Uppercase Letters": sans_serif_bold_uppercase,
    "Sans-Serif Bold Lowercase Letters": sans_serif_bold_lowercase,
    "Sans-Serif Italic Uppercase Letters": sans_serif_italic_uppercase,
    "Sans-Serif Italic Lowercase Letters": sans_serif_italic_lowercase,
    "Sans-Serif Bold Italic Uppercase Letters": sans_serif_bold_italic_uppercase,
    "Sans-Serif Bold Italic Lowercase Letters": sans_serif_bold_italic_lowercase,
    "Monospace Uppercase Letters": monospace_uppercase,
    "Monospace Lowercase Letters": monospace_lowercase,
}

for category, (start, end) in categories.items():
    print(f"{category}: {generate_unicode_range(start, end)}")

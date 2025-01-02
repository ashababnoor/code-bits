def generate_unicode_range(start, end):
    return [chr(i) for i in range(start, end)]

# Mathematical Bold Uppercase Letters
Mathematical_Bold_Uppercase = generate_unicode_range(0x1D400, 0x1D41A)

# Mathematical Bold Lowercase Letters
Mathematical_Bold_Lowercase = generate_unicode_range(0x1D41A, 0x1D434)

# Mathematical Italic Uppercase Letters
Mathematical_Italic_Uppercase = generate_unicode_range(0x1D434, 0x1D44E)

# Mathematical Italic Lowercase Letters
Mathematical_Italic_Lowercase = generate_unicode_range(0x1D44e, 0x1D468)

# Mathematical Bold Italic Uppercase Letters
Mathematical_Bold_Italic_Uppercase = generate_unicode_range(0x1D468, 0x1D482)

# Mathematical Bold Italic Lowercase Letters
Mathematical_Bold_Italic_Lowercase = generate_unicode_range(0x1D482, 0x1D49C)

# Mathematical Script Uppercase Letters
Mathematical_Script_Uppercase = generate_unicode_range(0x1D49C, 0x1D4B6)

# Mathematical Script Lowercase Letters
Mathematical_Script_Lowercase = generate_unicode_range(0x1D4B6, 0x1D4D0)

# ---

# Mathematical Bold Script Uppercase Letters
Mathematical_Bold_Script_Uppercase = generate_unicode_range(0x1D4D0, 0x1D4EA)

# Mathematical Bold Script Lowercase Letters
Mathematical_Bold_Script_Lowercase = generate_unicode_range(0x1D4EB, 0x1D505)

# Mathematical Fraktur Uppercase Letters
Mathematical_Fraktur_Uppercase = generate_unicode_range(0x1D504, 0x1D51E)

# Mathematical Fraktur Lowercase Letters
Mathematical_Fraktur_Lowercase = generate_unicode_range(0x1D51F, 0x1D539)

# Mathematical Double-Struck Uppercase Letters
Mathematical_Double_Struck_Uppercase = generate_unicode_range(0x1D538, 0x1D552)

# Mathematical Double-Struck Lowercase Letters
Mathematical_Double_Struck_Lowercase = generate_unicode_range(0x1D553, 0x1D56D)

# Sans-Serif Bold Uppercase Letters
Sans_Serif_Bold_Uppercase = generate_unicode_range(0x1D5A0, 0x1D5BA)

# Sans-Serif Bold Lowercase Letters
Sans_Serif_Bold_Lowercase = generate_unicode_range(0x1D5BB, 0x1D5D5)

# Sans-Serif Italic Uppercase Letters
Sans_Serif_Italic_Uppercase = generate_unicode_range(0x1D608, 0x1D622)

# Sans-Serif Italic Lowercase Letters
Sans_Serif_Italic_Lowercase = generate_unicode_range(0x1D623, 0x1D63D)

# Sans-Serif Bold Italic Uppercase Letters
Sans_Serif_Bold_Italic_Uppercase = generate_unicode_range(0x1D63C, 0x1D656)

# Sans-Serif Bold Italic Lowercase Letters
Sans_Serif_Bold_Italic_Lowercase = generate_unicode_range(0x1D657, 0x1D671)

# Monospace Uppercase Letters
Monospace_Uppercase = generate_unicode_range(0x1D670, 0x1D68A)

# Monospace Lowercase Letters
Monospace_Lowercase = generate_unicode_range(0x1D68B, 0x1D6A5)

categories = {
    "Mathematical Bold Uppercase Letters": Mathematical_Bold_Uppercase,
    "Mathematical Bold Lowercase Letters": Mathematical_Bold_Lowercase,
    "Mathematical Italic Uppercase Letters": Mathematical_Italic_Uppercase,
    "Mathematical Italic Lowercase Letters": Mathematical_Italic_Lowercase,
    "Mathematical Bold Italic Uppercase Letters": Mathematical_Bold_Italic_Uppercase,
    "Mathematical Bold Italic Lowercase Letters": Mathematical_Bold_Italic_Lowercase,
    "Mathematical Script Uppercase Letters": Mathematical_Script_Uppercase,
    "Mathematical Script Lowercase Letters": Mathematical_Script_Lowercase,
    "Mathematical Bold Script Uppercase Letters": Mathematical_Bold_Script_Uppercase,
    "Mathematical Bold Script Lowercase Letters": Mathematical_Bold_Script_Lowercase,
    "Mathematical Fraktur Uppercase Letters": Mathematical_Fraktur_Uppercase,
    "Mathematical Fraktur Lowercase Letters": Mathematical_Fraktur_Lowercase,
    "Mathematical Double-Struck Uppercase Letters": Mathematical_Double_Struck_Uppercase,
    "Mathematical Double-Struck Lowercase Letters": Mathematical_Double_Struck_Lowercase,
    "Sans-Serif Bold Uppercase Letters": Sans_Serif_Bold_Uppercase,
    "Sans-Serif Bold Lowercase Letters": Sans_Serif_Bold_Lowercase,
    "Sans-Serif Italic Uppercase Letters": Sans_Serif_Italic_Uppercase,
    "Sans-Serif Italic Lowercase Letters": Sans_Serif_Italic_Lowercase,
    "Sans-Serif Bold Italic Uppercase Letters": Sans_Serif_Bold_Italic_Uppercase,
    "Sans-Serif Bold Italic Lowercase Letters": Sans_Serif_Bold_Italic_Lowercase,
    "Monospace Uppercase Letters": Monospace_Uppercase,
    "Monospace Lowercase Letters": Monospace_Lowercase,
}

for category, letters in categories.items():
    print(f"{category}: {letters}")


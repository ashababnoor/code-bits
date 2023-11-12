
Latin1_Supplement_Digits = [chr(i) for i in range(0x0030, 0x003a)]

Fullwidth_Digits = [chr(i) for i in range(0xff10, 0xff1a)]

Mathematical_Bold_Digits = [chr(i) for i in range(0x1d7ce, 0x1d7d8)]

Mathematical_Double_Struck_Digits = [chr(i) for i in range(0x1d7d8, 0x1d7e2)]

Mathematical_Sans_Serif_Digits = [chr(i) for i in range(0x1d7e2, 0x1d7ec)]

Mathematical_Sans_Serif_Bold_Digits = [chr(i) for i in range(0x1d7ec, 0x1d7f6)]

Mathematical_Monospace_Digits = [chr(i) for i in range(0x1d7f6, 0x1d800)]

# ---

Circled_Digits = [chr(i) for i in range(0x2460, 0x246a)]

Dingbat_Negative_Circled_Digits = [chr(i) for i in range(0x2775, 0x2780)]

Dingbats = [chr(0x1f10b)] + [chr(i) for i in range(0x2780, 0x2789)]

Enclosed_Digits = [chr(i) for i in range(0x24b6, 0x24bf)]

Subscript_Digits = [chr(i) for i in range(0x2080, 0x208a)]

Superscript_Digits = [chr(i) for i in range(0x2070, 0x207a)]

print(f"Latin1_Supplement_Digits            {Latin1_Supplement_Digits}")
print(f"Fullwidth_Digits                    {Fullwidth_Digits}")
print(f"Mathematical_Bold_Digits            {Mathematical_Bold_Digits}")
print(f"Mathematical_Double_Struck_Digits   {Mathematical_Double_Struck_Digits}")
print(f"Mathematical_Sans_Serif_Digits      {Mathematical_Sans_Serif_Digits}")
print(f"Mathematical_Sans_Serif_Bold_Digits {Mathematical_Sans_Serif_Bold_Digits}")
print(f"Mathematical_Monospace_Digits       {Mathematical_Monospace_Digits}")

print(f"Circled_Digits                      {Circled_Digits}")
print(f"Dingbat_Negative_Circled_Digits     {Dingbat_Negative_Circled_Digits}")
print(f"Dingbats                            {Dingbats}")
print(f"Enclosed_Digits                     {Enclosed_Digits}")
print(f"Subscript_Digits                    {Subscript_Digits}")
print(f"Superscript_Digits                  {Superscript_Digits}")
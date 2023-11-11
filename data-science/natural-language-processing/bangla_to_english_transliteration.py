'''
The following functions were generated by ChatGPT 3.5
They do not work as the name suggests. Use with caution.
'''

def bangla_to_english_transliteration(bangla_text):
    mapping = {
        'অ': 'a', 'আ': 'a', 'ই': 'i', 'ঈ': 'i', 'উ': 'u', 'ঊ': 'u', 'ঋ': 'ri', 'এ': 'e', 'ঐ': 'oi', 'ও': 'o', 'ঔ': 'ou',
        'ক': 'k', 'খ': 'kh', 'গ': 'g', 'ঘ': 'gh', 'ঙ': 'ng',
        'চ': 'ch', 'ছ': 'chh', 'জ': 'j', 'ঝ': 'jh', 'ঞ': 'n',
        'ট': 't', 'ঠ': 'th', 'ড': 'd', 'ঢ': 'dh', 'ণ': 'n',
        'ত': 't', 'থ': 'th', 'দ': 'd', 'ধ': 'dh', 'ন': 'n',
        'প': 'p', 'ফ': 'ph', 'ব': 'b', 'ভ': 'bh', 'ম': 'm',
        'য': 'j', 'র': 'r', 'ল': 'l', 'শ': 'sh', 'ষ': 'sh',
        'স': 's', 'হ': 'h', '়': '', 'ঽ': '', 'া': 'a',
        'ি': 'i', 'ী': 'i', 'ু': 'u', 'ূ': 'u', 'ৃ': 'ri', 'ে': 'e', 'ৈ': 'oi', 'ো': 'o', 'ৌ': 'ou',
        '্': '', 'ৎ': '', '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4', '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9'
    }

    english_text = ''.join([mapping.get(char, char) for char in bangla_text])
    return english_text


def english_to_bangla_reverse_transliteration(english_text):
    reverse_mapping = {
        'a': 'অ', 'i': 'ই', 'u': 'উ', 'ri': 'ঋ', 'e': 'এ', 'oi': 'ঐ', 'o': 'ও', 'ou': 'ঔ',
        'k': 'ক', 'kh': 'খ', 'g': 'গ', 'gh': 'ঘ', 'ng': 'ঙ',
        'ch': 'চ', 'chh': 'ছ', 'j': 'জ', 'jh': 'ঝ', 'n': 'ঞ',
        't': 'ট', 'th': 'ঠ', 'd': 'ড', 'dh': 'ঢ', 'n': 'ণ',
        'p': 'প', 'ph': 'ফ', 'b': 'ব', 'bh': 'ভ', 'm': 'ম',
        'j': 'য', 'r': 'র', 'l': 'ল', 'sh': 'শ', 's': 'স', 'h': 'হ',
        '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'
    }

    bangla_text = ''.join([reverse_mapping.get(char, char) for char in english_text])
    return bangla_text


if __name__ == "__main__":
    
    # Example Usage of english_to_bangla_transliteration
    english_text = "ami banglay kotha boli"
    bangla_text = english_to_bangla_reverse_transliteration(english_text)
    print(f"Example of: {english_to_bangla_reverse_transliteration.__name__}")
    print(f"{english_text = }; {bangla_text = }")

    print()

    # Example Usage of bangla_to_english_transliteration
    bangla_text = "আমি বাংলায় কথা বলি"
    english_text = bangla_to_english_transliteration(bangla_text)
    print(f"Example of: {bangla_to_english_transliteration.__name__}")
    print(f"{bangla_text = }; {english_text = }")
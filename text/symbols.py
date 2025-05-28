""" from https://github.com/keithito/tacotron """

from text import bndict

# _pad        = '_'
# _punctuation = '!\'(),.:;? '
# _special = '-'
# _letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

# # Prepend "@" to ARPAbet symbols to ensure uniqueness:
# _arpabet = ['@' + s for s in cmudict.valid_symbols]

# Export all symbols:
# symbols = [_pad] + list(_special) + list(_punctuation) + list(_letters) + _arpabet
_PUNCTUATION = ['!', ',', '.', '?']
_IPA = bndict.valid_symbols

symbols = [
    '_', '~', ' ', *_PUNCTUATION, 'a', 'à', 'ả', 'ã', 'á', 'ạ', 
    'ă', 'ằ', 'ẳ', 'ẵ', 'ắ', 'ặ', 'â', 'ầ', 'ẩ', 'ẫ', 'ấ', 'ậ', 
    'b', 'c', 'd', 'đ', 'e', 'è', 'ẻ', 'ẽ', 'é', 'ẹ', 'ê', 'ề', 
    'ể', 'ễ', 'ế', 'ệ', 'f', 'g', 'h', 'i', 'ì', 'ỉ', 'ĩ', 'í', 
    'ị', 'j', 'k', 'l', 'm', 'n', 'o', 'ò', 'ỏ', 'õ', 'ó', 'ọ', 
    'ô', 'ồ', 'ổ', 'ỗ', 'ố', 'ộ', 'ơ', 'ờ', 'ở', 'ỡ', 'ớ', 'ợ', 
    'p', 'q', 'r', 's', 't', 'u', 'ù', 'ủ', 'ũ', 'ú', 'ụ', 'ư', 
    'ừ', 'ử', 'ữ', 'ứ', 'ự', 'v', 'w', 'x', 'y', 'ỳ', 'ỷ', 'ỹ', 
    'ý', 'ỵ', 'z', *_IPA
]

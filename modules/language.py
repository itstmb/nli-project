"""
Language families: Germanic, BaltoSlavic, NativeEnglish ,Other, Latin

"""

class Language(object):
    def __init__(self, native, family, language_name):
        self.native = native
        self.family = family
        self.language_name = language_name

LanguageDict = {
    'Albania': Language(False, 'Other', 'Albania'),
    'Armenia': Language(False, 'Other', 'Armenia'),
    'Australia': Language(True, 'NativeEnglish', 'English'),
    'Austria': Language(False, 'Germanic', 'German'),
    'Bosnia': Language(False, 'BaltoSlavic', 'Bosnia'),
    'Bulgaria': Language(False, 'BaltoSlavic', 'Bulgaria'),
    'Canada': Language(True, 'NativeEnglish', 'English'),
    'China': Language(False, 'Other', 'China'),
    'Croatia': Language(False, 'BaltoSlavic', 'Croatia'),
    'Cyprus': Language(False, 'Other', 'Greece'),
    'Czech': Language(False, 'BaltoSlavic', 'Czech'),
    'Denmark': Language(False, 'Germanic', 'Denmark'),
    'Estonia': Language(False, 'BaltoSlavic', 'Estonia'),
    'Finland': Language(False, 'Other' , 'Finland'),
    'France': Language(False, 'Latin', 'France'),
    'Georgia': Language(False, 'Other', 'Georgia'),
    'Germany': Language(False, 'Germanic', 'German'),
    'Greece': Language(False, 'Other', 'Greece'),
    'Hungary': Language(False, 'Other', 'Hungary'),
    'Iceland': Language(False, 'Germanic', 'Iceland'),
    'Ireland': Language(True, 'NativeEnglish', 'English'),
    'India': Language(False, 'Other', 'India'),
    'Israel': Language(False, 'Other', 'Israel'),
    'Italy': Language(False, 'Latin', 'Italy'),
    'Latvia': Language(False, 'BaltoSlavic', 'Latvia'),
    'Lithuania': Language(False, 'BaltoSlavic', 'Lithuania'),
    'Macedonia': Language(False, 'BaltoSlavic', 'Macedonia'),
    'Malta': Language(False, 'Latin', 'Malta'),
    'Mexico': Language(False, 'Latin', 'Spanish'),
    'Moldova': Language(False, 'Latin', 'Romania'),
    'Montenegro': Language(False, 'BaltoSlavic', 'Montenegro'),
    'Netherlands': Language(False, 'Germanic', 'Netherlands'),
    'NewZealand': Language(True, 'NativeEnglish', 'English'),
    'Norway': Language(False, 'Germanic' , 'Norway'),
    'Poland': Language(False, 'BaltoSlavic', 'Poland'),
    'Portugal': Language(False, 'Latin', 'Portugal'),
    'Romania': Language(False, 'Latin', 'Romania'),
    'Russia': Language(False, 'BaltoSlavic', 'Russia'),
    'Serbia': Language(False, 'BaltoSlavic', 'Serbia'),
    'Slovakia': Language(False, 'BaltoSlavic',  'Slovakia'),
    'Slovenia': Language(False, 'BaltoSlavic', 'Slovenia'),
    'Spain': Language(False, 'Latin', 'Spanish'),
    'Sweden': Language(False, 'Germanic', 'Sweden'),
    'Turkey': Language(False, 'Other', 'Turkey'),
    'UK': Language(True, 'NativeEnglish', 'English'),
    'Ukraine': Language(False, 'BaltoSlavic', 'Ukraine'),
    'US': Language(True, 'NativeEnglish', 'English'),
    'Vietnam': Language(False, 'Other', 'Vietnam')
}

# Maps language families to numbers for family classification
FamilyToNum = {
    'Germanic': 0,
    'BaltoSlavic': 1,
    'NativeEnglish': 2,
    'Latin': 3,
    'Other': 4
}

"""
Language families:     Germanic, BaltoSlavic, Romance, NativeEnglish ,Albanian, Armenian, NonEuropean,
                       Finno-Permic, AfroAsiatic, Turkic, Hellenic, Finnic, Karto-Zan
"""

class Language(object):
    def __init__(self, native, family, language_name):
        self.native = native
        self.family = family
        self.language_name = language_name

LanguageDict = {
        'Albania': Language(False, 'Albanian', 'Albania'),
        'Armenia': Language(False, 'Armenian', 'Armenia'),
        'Australia': Language(True, 'NativeEnglish', 'English'),
        'Austria': Language(False, 'Germanic', 'German'),
        'Bosnia': Language(False, 'BaltoSlavic', 'Bosnia'),
        'Bulgaria': Language(False, 'BaltoSlavic', 'Bulgaria'),
        'Canada': Language(True, 'NativeEnglish', 'English'),
        'China': Language(False, 'NonEuropean', 'China'),
        'Croatia': Language(False, 'BaltoSlavic', 'Croatia'),
        'Cyprus': Language(False, 'Hellenic', 'Greece'),
        'Czech': Language(False, 'BaltoSlavic', 'Czech'),
        'Denmark': Language(False, 'Germanic', 'Denmark'),
        'Estonia': Language(False, 'Finnic', 'Estonia'),
        'Finland': Language(False, 'Finnic', 'Finland'),
        'France': Language(False, 'Romance', 'France'),
        'Georgia': Language(False, 'Karto-Zan', 'Georgia'),
        'Germany': Language(False, 'Germanic', 'German'),
        'Greece': Language(False, 'Hellenic', 'Greece'),
        'Hungary': Language(False, 'Finno-Permic', 'Hungary'),
        'Iceland': Language(False, 'Germanic', 'Iceland'),
        'Ireland': Language(True, 'NativeEnglish', 'English'),
        'India': Language(False, 'NonEuropean', 'India'),
        'Israel': Language(False, 'AfroAsiatic', 'Israel'),
        'Italy': Language(False, 'Romance', 'Italy'),
        'Latvia': Language(False, 'BaltoSlavic', 'Latvia'),
        'Lithuania': Language(False, 'BaltoSlavic', 'Lithuania'),
        'Macedonia': Language(False, 'BaltoSlavic', 'Macedonia'),
        'Malta': Language(False, 'AfroAsiatic', 'Malta'),
        'Mexico': Language(False, 'Romance', 'Spanish'),
        'Moldova': Language(False, 'Romance', 'Romania'),
        'Montenegro': Language(False, 'BaltoSlavic', 'Montenegro'),
        'Netherlands': Language(False, 'Germanic', 'Netherlands'),
        'NewZealand': Language(True, 'NativeEnglish', 'English'),
        'Norway': Language(False, 'Germanic', 'Norway'),
        'Poland': Language(False, 'BaltoSlavic', 'Poland'),
        'Portugal': Language(False, 'Romance', 'Portugal'),
        'Romania': Language(False, 'Romance', 'Romania'),
        'Russia': Language(False, 'BaltoSlavic', 'Russia'),
        'Serbia': Language(False, 'BaltoSlavic', 'Serbia'),
        'Slovakia': Language(False, 'BaltoSlavic', 'Slovakia'),
        'Slovenia': Language(False, 'BaltoSlavic', 'Slovenia'),
        'Spain': Language(False, 'Romance', 'Spanish'),
        'Sweden': Language(False, 'Germanic', 'Sweden'),
        'Turkey': Language(False, 'Turkic', 'Turkey'),
        'UK': Language(True, 'NativeEnglish', 'English'),
        'Ukraine': Language(False, 'BaltoSlavic', 'Ukraine'),
        'US': Language(True, 'Turkic', 'English'),
        'Vietnam': Language(False, 'NonEuropean', 'Vietnam')
}

'''Germanic, BaltoSlavic, Romance, NativeEnglish ,Albanian, Armenian, NonEuropean,
                       Finno-Permic, AfroAsiatic, Turkic, Hellenic, Finnic, Karto-Zan'''

# Maps language families to numbers for family classification
FamilyToNum = {
        'Germanic': 0,
        'BaltoSlavic': 1,
        'Romance': 2,
        'NativeEnglish': 3,
        'Albanian': 4,
        'Armenian': 5,
        'NonEuropean': 6,
        'Finno-Permic': 7,
        'AfroAsiatic': 8,
        'Turkic': 9,
        'Hellenic': 10,
        'Finnic': 11,
        'Karto-Zan': 12
}
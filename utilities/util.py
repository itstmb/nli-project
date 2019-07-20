import os
import errno
import datetime
import random

import utilities.interpreter as setup

from ast import literal_eval

class Language(object):
    def __init__(self, native, family, name):
        self.native = native
        self.family = family
        self.name = name


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

# Maps languages to numbers for language classification
LanguageToNum = {
    'Albania': 0,
    'Armenia': 1,
    'English': 2,
    'German': 3,
    'Bosnia': 4,
    'Bulgaria': 5,
    'China': 6,
    'Croatia': 7,
    'Greece': 8,
    'Czech': 9,
    'Denmark': 10,
    'Estonia': 11,
    'Finland': 12,
    'France': 13,
    'Georgia': 14,
    'Hungary': 15,
    'Iceland': 16,
    'India': 17,
    'Israel': 18,
    'Italy': 19,
    'Latvia': 20,
    'Lithuania': 21,
    'Macedonia': 22,
    'Malta': 23,
    'Spanish': 24,
    'Romania': 25,
    'Montenegro': 26,
    'Netherlands': 27,
    'Norway': 28,
    'Poland': 29,
    'Portugal': 30,
    'Russia': 31,
    'Serbia': 32,
    'Slovakia': 33,
    'Slovenia': 34,
    'Sweden': 35,
    'Turkey': 36,
    'Ukraine': 37,
    'Vietnam': 38
}


FeatureToDirectory = {
    'trichar': '/char_ngrams_chunks.tar/char_ngrams_chunks',
    'pos': '/pos_chunks.tar/pos_chunks-004/pos_chunks',
    'unigrams' : '/text_chunks.tar/text_chunks',
    'functionwords' : '/text_chunks.tar/text_chunks',
    'synchronized_functionwords' : '/text_chunks.tar/text_chunks',
    'avg_word': '/text_chunks.tar/text_chunks',
    'english': '/text_chunks.tar/text_chunks',
    'bipos': '/pos_chunks.tar/pos_chunks-004/pos_chunks',
    'avgcapital': '/text_chunks.tar/text_chunks',
    'numberwords': '/text_chunks.tar/text_chunks',
    'punctuations': '/text_chunks.tar/text_chunks',
    'edit_distance': '/spell_checker_chunks.tar/spell_checker_chunks-005/spell_checker_chunks',
    'spelling_errors': '/spell_checker_chunks.tar/spell_checker_chunks-005/spell_checker_chunks',
    'country_words': '/text_chunks.tar/text_chunks'
}


CountryWords = {
    'albania': 0, 'albanian': 0,
    '           tung': 0, 'tirana': 0, 'durres': 0, 'vlore': 0, 'elbasan': 0, 
                   'shkoder': 0, 'byrek': 0, 'baklava': 0, 'trilece': 0, 'qofte': 0,

    'australia': 1,
                'sydney': 1, 'melbourne': 1, 'brisbane': 1, 'perth': 1, 'canberra': 1,
                'vegemite': 1, 'fairy-bread': 1, 'kangaroo': 1, 'meat pie': 1, 'pavlova': 1,

    'austria': 2, 'german': 2, 'hallo': 2,
                'vienna': 2, 'graz': 2, 'linz': 2, 'salzburg': 2, 'innsbruck': 2, 'klagenfurt': 2,
                'schnitzel': 2, 'goulash': 2, 'spargel': 2, 'melange': 2,

    'bosnia': 3, 'bosnian': 3, 'zdravo': 3,
               'sarajevo': 3, 'banja': 3, 'tuzla': 3, 'zenica': 3, 'bijeljina': 3,
               'cevapi': 3, 'burek': 3, 'begova': 3, 'dolma': 3, 'klepe': 3,

    'bulgaria': 4, 'bulgarian': 4, 'kakvo': 4,
                 'sofia': 4, 'plovdiv': 4, 'varna': 4, 'burgas': 4, 'ruse': 4,
                 'banitza': 4, 'lukanka': 4, 'shkembe': 4, 'tarator': 4, 'kebapche': 4,

    'canada': 5,
               'toronto': 5, 'montreal': 5, 'vancouver': 5, 'calgary': 5, 'edmonton': 5,
               'poutine': 5, 'bannock': 5, 'tarts': 5, 'beavertails': 5, 'maple': 5,

    'croatia': 6, 'croatian': 6, 'zdravo': 6,
                'zagreb': 6, 'rijeka': 6, 'osijek': 6, 'zadar': 6, 'velika': 6,
                'strukli': 6, 'manestra': 6, 'peka': 6, 'sarma': 6, 'brudet': 6,

    'czech-republic' 'czech': 7,
              'prague': 7, 'praha': 7, 'brno': 7, 'ostrava': 7, 'plzen': 7,
              'rizek': 7, 'uzene': 7, 'gulas': 7, 'goulash': 7,

    'denmark': 8, 'danish': 8, 'hej': 8,
                'copenhagen': 8, 'aarhus': 8, 'odense': 8, 'aalborg': 8, 'esbjerg': 8,
                'polser': 8, 'kartofler': 8, 'wienerbrod': 8, 'glogg': 8, 'risalamande': 8,

    'estonia': 9, 'estonian': 9, 'tere': 9,
                'tallinn': 9, 'tatru': 9, 'narva': 9, 'parnu': 9, 'viljandi': 9,
                'aspic': 9, 'kali': 9, 'semla': 9, 'kohuke': 9, 'kalev': 9,

    'finland': 10, 'finnish': 10,
                'helsinki': 10, 'espoo': 10, 'tampere': 10, 'vantaa': 10, 'oulu': 10,
                'kalakukko': 10, 'karjalanpiirakka': 10, 'grillimakkara': 10, 'ruisleipa': 10, 'korvapuusti': 10,

    'france': 11, 'french': 11, 'bonjour': 11,
               'paris': 11, 'marseille': 11, 'lyon': 11, 'toulouse': 11, 'monaco': 11,
               'cassoulet': 11, 'baguette': 11, 'flamiche': 11, 'ratatouille': 11, 'canard': 11,
               'eiffel': 11, 'louvre': 11, 'elysees': 11, 'musee': 11, 'triomphe': 11,

    'german': 12, 'germania': 12,
                'berlin': 12, 'hamburg': 12, 'munich': 12, 'munchen': 12, 'cologne': 12, 'koln': 12, 'frankfurt': 12, 'stuttgart': 12, 'dusseldorf'
                'rouladen': 12, 'grutze': 12, 'eintopf': 12, 'sauerbraten': 12, 'brezel': 12,

    'greece': 13, 'greek': 13, 'geia': 13,
               'athens': 13, 'thessaloniki': 13, 'patras': 13, 'larissa': 13, 'heraklion': 13,
               'taramasalata': 13, 'feta': 13, 'moussaka': 13,

    'hungary': 14, 'hungarian': 14, 'szia': 14,
                'budapest': 14, 'debrecen': 14, 'szeged': 14, 'miskolc': 14, 'gyor': 14,
                'langos': 14, 'gulyas': 14, 'goulash': 14, 'dobostorta': 14, 'meggyleves': 14,

    'iceland': 15, 'icelandic': 15,
                'reykjavík': 15, 'akureyri': 15, 'kopavogur': 15, 'selfoss': 15, 'akranes': 15,
                'svid': 15, 'pylsur': 15, 'brennivin': 15, 'skyr': 15, 'puffin': 15,

    'ireland': 16, 'irish': 16,
                'dublin': 16, 'cork': 16, 'limerick': 16, 'galway': 16, 'waterford': 16,
                'shellfish': 16, 'colcannon': 16, 'boxty': 16, 'pudding': 16, 'barmbrack': 16,

    'italy': 17, 'italian': 17, 'ciao': 17,
              'rome': 17, 'milan': 17, 'naples': 17, 'turin': 17, 'palermo': 17, 'venice': 17,
              'bottarga': 17, 'lasagna': 17, 'fiorentina': 17, 'ribolita': 17, 'gelato': 17,

    'latvia': 18, 'latvian': 18, 'sveiki': 18,
               'daugavpils': 18, 'jekavpils': 18, 'jelgava': 18, 'jurmala': 18, 'liepaja': 18,
               'speck': 18, 'kvass': 18, 'dill': 18,

    'lithuania': 19, 'lithuanian': 19, 'sveiki': 19,
                  'vilnius': 19, 'kaunas': 19, 'klaipeda': 19, 'siauliai': 19, 'panevezys': 19,
                  'cepelinai': 19, 'kepta': 19, 'borscht': 19, 'grybukai': 19, 'kibinai': 19,

    'netherlands': 20, 'holland': 20,
                    'amsterdam': 20, 'rotterdam': 20, 'hague': 20, 'utrecht': 20, 'eindhoven': 20,
                    'stroopwafel': 20, 'korket': 20, 'patat': 20, 'poffertjes': 20, 'bitterballen': 20,

    'norway': 21, 'norwegian': 21,
               'oslo': 21, 'bergen': 21, 'sandnes': 21, 'trondheim': 21, 'drammen': 21,
               'lefse': 21, 'klippfisk': 21, 'svele': 21, 'raspeballer': 21, 'rakfisk': 21,

    'poland': 22, 'polish': 22, 'dzien': 22,
               'karkow': 22, 'lodz': 22, 'wroclaw': 22, 'poznan': 22, 'gdansk': 22,
               'pierogi': 22, 'rosol': 22, 'golabki': 22, 'polskie': 22, 'lazanki': 22,

    'portugal': 23, 'portuguese': 23, 'portuguesa': 23, 'ola': 23,
                 'lisbon': 23, 'porto': 23, 'braga': 23, 'coimbra': 23, 'funchal': 23,
                 'sardinhas': 23, 'cozido': 23, 'acorda': 23, 'peixinhos': 23, 'feijoada': 23,

    'romania': 24, 'romanian': 24, 'salut': 24,
                'bucharest': 24, 'cluj': 24, 'timis': 24, 'iasi': 24, 'constanta': 24,
                'sarmale': 24, 'ciorba': 24, 'balmos': 24, 'jumari': 24, 'mici': 24,

    'russia': 25, 'russian': 25, 'privet': 25,
               'moscow': 25, 'petersburg': 25, 'novosibirsk': 25, 'yekaterinburg': 25, 'kazan': 25,
               'borscht': 25, 'shchi': 25, 'solyanka': 25, 'ukha': 25, 'pirozhki': 25,

    'serbia': 26, 'serbian': 26, 'zdravo': 26,
               'belgrade': 26, 'nis': 26, 'kragujevac': 26, 'leskovac': 26, 'subotica': 26,
               'kajmak': 26, 'sarma': 26, 'musaka': 26, 'ajvar': 26, 'kobasice': 26,

    'slovakia': 27, 'slovak': 27, 'ahoj': 27,
                 'bratislava': 27, 'kosice': 27, 'presov': 27, 'zilina': 27, 'nitra': 27,
                 'bryndza': 27, 'goulash': 27, 'schnitzel': 27, 'funnel': 27,

    'slovenia': 28, 'slovene': 28, 'zdravo': 28,
                 'ljubljana': 28, 'maribor': 28, 'celje': 28, 'kranj': 28, 'koper': 28,
                 'kranjska': 28, 'potica': 28, 'gibanica': 28, 'kraski': 28, 'struklji': 28,

    'spain': 29, 'spanish': 29, 'espana': 29, 'hola': 29,
              'madrid': 29, 'barcelona': 29, 'valencia': 29, 'seville': 29, 'bilbao': 29,
              'croquettes': 29, 'tortilla': 29, 'espanola': 29, 'pisto': 29, 'paella': 29,

    'sweden': 30, 'swedish': 30, 'hej': 30,
               'stockholm': 30, 'gothenburg': 30, 'malmo': 30, 'uppsala': 30, 'linkoping': 30,
               'jansson': 30, 'raggmunk': 30, 'chives': 30, 'gubbrora': 30, 'skagen': 30,

    'turkey': 31, 'turkish': 31, 'merhaba': 31,
               'istanbul': 31, 'ankara': 31, 'izmir': 31, 'bursa': 31, 'adana': 31,
               'menemen': 31, 'kofte': 31, 'lokum': 31, 'baklava': 31, 'lahmacun': 31,

    'england': 32, 'uk': 32, 'britain': 32, 'british'
           'london': 32, 'liverpool': 32, 'manchester': 32, 'birmingham': 32, 'leeds': 32,
           'eccles': 32, 'pudding': 32, 'laverbread': 32, 'yorkshire': 32, 'haggis': 32,

    'ukraine': 33, 'ukrainian': 33, 'zdrastuyte': 33,
                'kyiv': 33, 'kharkiv': 33, 'odessa': 33, 'dnipro': 33, 'donetsk': 33,
                'borscht': 33, 'kiev': 33, 'salo': 33, 'vareniki': 33, 'okroshka': 33,

    'us': 34, 'usa': 34, 'america': 34, 'unitedstates': 34, 'american': 34,
           'york': 34, 'angeles': 34, 'chicago': 34, 'houston': 34, 'dallas': 34, 'california': 34,
           'twinkies': 34, 'cornbread': 34, 'meatloaf': 34, 'maryland': 34, 'buffalo': 34
}


def get_time():
    return datetime.datetime.now().strftime("%X")


# Takes 2 vectors and shuffles while keeping them in the same {a,b} fitting.
def shuffle_vectors(vector_a, vector_b):
    combined_vector = list(zip(vector_a,vector_b))
    random.shuffle(combined_vector)
    vector_a, vector_b = zip(*combined_vector)
    return vector_a, vector_b


def exists(path):
    if path.is_file():
        return True
    return False


def save_file(path, data_list):

    # check / create directory
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # write file
    with open(path, 'w') as f:
        for data in data_list:
            f.write('%s\n' % data)
    f.close()


def write_scores(score):
    score_info = '[{}]:\n' \
                 'feature: {}\n' \
                 'type: {}\n' \
                 'domain: {}\n' \
                 'threads: {}\n' \
                 'max iterations: {}\n' \
                 'score: {}'.format(get_time(),
                                    setup.feature,
                                    setup.type,
                                    setup.domain,
                                    setup.threads,
                                    setup.iterations,
                                    score)

    write_to_file(score_info)


def write_to_file(data):
    with open('results.txt', 'a') as f:
        f.write('______\n%s\n' % data)


def load_file(path):
    try:
        with open(path) as f:
            data = f.read().splitlines()
    except IOError:
        raise IOError('Error: Error loading file from path: ', path)
    return data

def load_users(path):
    try:
        in_users = [literal_eval(line) for line in open(path, 'r')]
    except IOError:
        print ("Error: File does not appear to exist.")
        return 0

    return in_users



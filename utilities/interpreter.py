import utilities.util as util


possible_inputs = {
    0: ['trichar',
        'pos',
        'unigrams',
        'functionwords',
        'synchronized_functionwords',
        'avg_word',
        'english',
        'bipos',
        'avgcapital',
        'numberwords',
        'punctuations',
        'edit_distance',
        'spelling_errors',
        'country_words'],
    1: ['binary','family', 'language'],
    2: ['in', 'out'],
    3: [x for x in range(-1, 17)]
}

'''
feature: [trichar/pos]
type: [binary/family/language]
domain: [in/out]
threads: [-1 - 16]
'''


def get_params():
    global feature, type, domain, threads, iterations, numOfFunctionwords
    feature = input('Feature? ' + str(possible_inputs[0]) + ' : ')
    if feature == 'synchronized_functionwords':
        numOfFunctionwords= int(input('numOfFunctionwords?: '))
    type = input('Classification type? ' + str(possible_inputs[1]) + ' : ')
    domain = input('Domain? ' + str(possible_inputs[2]) + ' : ')
    threads = int(input('Number of threads? [-1 - 16] : '))
    iterations = int(input('Maximum iterations? [-1-1,000,000] : '))

    for index, x in enumerate([feature, type, domain, threads]):
        if x not in possible_inputs[index]:
            raise IOError("Bad input! '{}' not in {}".format(x, possible_inputs[index]))

    get_database()

def set_params(gui_feature, gui_type, gui_domain, gui_threads, gui_iterations, gui_numOfFunctionWords = 0):
    global feature, type, domain, threads, iterations, numOfFunctionwords
    feature = gui_feature
    type = gui_type
    domain = gui_domain
    threads = gui_threads
    iterations = gui_iterations
    if feature == 'synchronized_functionwords':
        numOfFunctionwords = gui_numOfFunctionWords

    get_database()


def get_database():
    global database
    database = util.load_file('utilities/database_dir.txt')[0] + util.FeatureToDirectory[feature]
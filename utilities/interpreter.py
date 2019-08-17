import utilities.util as util


possible_inputs = {
    0: ['None',
        'trichar',
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
    feature = input('Feature? ' + str(possible_inputs[0][1:]) + ' : ')
    if feature == 'synchronized_functionwords':
        numOfFunctionwords= int(input('numOfFunctionwords?: '))
    feature2 = input('Feature 2? ' + str(possible_inputs[0]) + ' : ')
    type = input('Classification type? ' + str(possible_inputs[1]) + ' : ')
    domain = input('Domain? ' + str(possible_inputs[2]) + ' : ')
    threads = int(input('Number of threads? [-1 - 16] : '))
    iterations = int(input('Maximum iterations? [-1-1,000,000] : '))

    for index, x in enumerate([feature, type, domain, threads]):
        if x not in possible_inputs[index]:
            raise IOError("Bad input! '{}' not in {}".format(x, possible_inputs[index]))

    get_database()


def set_params(var_feature, var_feature2, var_type, var_domain, var_threads, var_iterations, var_numOfFunctionWords = 0):
    global feature, feature2, type, domain, threads, iterations, numOfFunctionwords
    feature = var_feature
    feature2 = var_feature2
    type = var_type
    domain = var_domain
    threads = var_threads
    iterations = var_iterations
    if feature == 'synchronized_functionwords':
        numOfFunctionwords = var_numOfFunctionWords

    get_database()


def get_database():
    global database
    database = util.load_file('utilities/database_dir.txt')[0] + util.FeatureToDirectory[feature]
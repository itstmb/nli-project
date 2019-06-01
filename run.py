from logger import log
import interpreter as i
import util
from classifier.classifier import classify
from vectors_handling.vector_provider import provide_vectors

'''import indomain_classifier
import outdomain_classifier'''


if __name__ == '__main__':
    log('Starting NLI with user generated content')

    i.get_params()  # Input handling

    users, countries = provide_vectors()  # Generate vectors for the classification task

    #  For out-domain, require in domain vectors as well
    if i.domain == 'out':
        i.domain = 'in'
        in_users, in_countries = provide_vectors()
        i.domain = 'out'
        result = classify(users, countries, in_users, in_countries)

    else:
        result = classify(users, countries)

    util.write_to_file(result)
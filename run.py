import utilities.interpreter as setup
import utilities.util as util
from classifier.classifier import classify
from vectors_handling.vector_provider import provide_vectors
import gui_interface as gui

'''import indomain_classifier
import outdomain_classifier'''


if __name__ == '__main__':
    gui.GuiInterface()

    '''
    log('Starting NLI with user generated content')
    setup.get_params()  # Input handling

    users, countries = provide_vectors()  # Generate vectors for the classification task

    #  For out-domain, require in domain vectors as well
    if setup.domain == 'out':
        setup.domain = 'in'
        in_users, in_countries = provide_vectors()
        setup.domain = 'out'
        result = classify(users, countries, in_users, in_countries)

    else:
        result = classify(users, countries)

    util.write_scores(result)
    '''


import sys
import globals

from classifiers.char_ngrams import classifier

if __name__ == '__main__':
    print ("~NLIWUGC~")
    globals.initialize()  # init global variables
    print("[",globals.start_time,"] run started")
    if len(sys.argv) == 1:
        classifier.char_ngrams_classifier(False)
    elif len(sys.argv) == 2:
        classifier.char_ngrams_classifier(True, sys.argv[1])
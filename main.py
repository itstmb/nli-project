import sys
import globals

from classifiers.char_ngrams import classifier


# syntax: python main.py trichar/pos in/out binary/family/language database_directory
def input_interpeter(argv):
    num_components = len(argv)
    if num_components not in {4,5}:  # only allow either 3 or 4 parameters.
        raise NameError("Input too short. please use the correct syntax.")
    else:
        if  argv[2] in {"in","out"} and argv[3] in {"binary","family","language"}:
            if argv[1] == "trichar":
                if num_components == 4: # load vectors
                    classifier.char_ngrams_classifier(False, argv[2], argv[3])
                elif num_components == 5: # generate vectors
                    classifier.char_ngrams_classifier(True, argv[2], argv[3], argv[4])
            elif argv[1] == "pos":
                print("Yet to be implemented.")

if __name__ == '__main__':
    print ("~NLIWUGC~")
    globals.initialize()  # init global variables
    print("[",globals.start_time,"] run started")
    input_interpeter(sys.argv)
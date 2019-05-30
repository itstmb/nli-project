import sys
import globals

from classifiers import classifier
# from classifiers.pos import classifier


# syntax: python main.py trichar/pos in/out binary/family/language #threads database_directory
def input_interpeter(argv):
    num_components = len(argv)
    if num_components not in {5,6}:  # only allow either 3 or 4 parameters.
        raise NameError("Input too short. please use the correct syntax.")
    else:
        if  argv[2] in {"in","out"} and argv[3] in {"binary","family","language"}:
            if num_components == 5: # load vectors
                classifier.classifier(generate_vectors=False,
                                      feature=argv[1],
                                      in_out_domain=argv[2],
                                      vector_type=argv[3],
                                      util_threads=int(argv[4]))
            elif num_components == 6: # generate vectors
                classifier.classifier(generate_vectors=True,
                                      feature=argv[1],
                                      in_out_domain=argv[2],
                                      vector_type=argv[3],
                                      util_threads=int(argv[4]),
                                      database_dir=argv[5])

if __name__ == '__main__':
    print ("~NLIWUGC~")
    globals.initialize()  # init global variables
    print("[",globals.start_time,"] run started")
    input_interpeter(sys.argv)
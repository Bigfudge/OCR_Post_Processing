import word_classifier
import constants as c
import sys
import helper_funtions as h
import post_processing as p


def post_processing_file(input_file, output_file=False):
    sample_size = 0

    if not h.is_non_zero_file(input_file):
        print("Input file is empty or do not exsist.")
        return

    if '-c' in sys.argv:
        p.clean_run()
    if '-ss' in sys.argv:
        sample_size = 30
    if '-v' in sys.argv:
        c.verbose = True

    number_of_vectors_from_each_source = 8000
    size_training_data = 10000
    svm_kernal = "rbf"
    c_value = 1
    gamma = 1
    max_words = 10000
    max_trigrams = 15000
    max_edit_distance = 8
    min_edit_distance = 0

    conf = p.Configuration(number_of_vectors_from_each_source,
                           size_training_data,
                           svm_kernal,
                           c_value,
                           gamma,
                           max_words,
                           max_trigrams,
                           max_edit_distance,
                           min_edit_distance,
                           sample_size)

    data = p.DataSet(conf)
    svm_model, performace_report = word_classifier.train(conf)

    corrected_text = p.process_file(input_file, svm_model, data, conf)

    if output_file:
        with open(output_file, 'w') as fd:
            for word in corrected_text:
                fd.write("%s " % word)
    else:
        print(' '.join(corrected_text))

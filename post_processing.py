import build_data_structure
import word_classifier
import error_correction
import os
import constants as c
import sys
import accuracyScript
import helper_funtions as h
import word_features


def process_dir(input_dir, output_dir, svm_model, data_set, conf):
    count = 0
    for file_name in os.listdir(input_dir):
        if conf.sample_size != 0 and count >= conf.sample_size:
            return
        count += 1

        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)

        corrected_text = process_file(input_path, svm_model, data_set, conf)

        with open(output_path, 'w') as f:
            for item in corrected_text:
                f.write("%s " % item)


def process_file(input_file, svm_model, data_set, conf):
    words = h.get_txt_from_file(input_file)
    filtered_words = h.filter_text(words)
    feature_vectors = []

    for word in filtered_words:
        feature_vectors.append([word,
                                word_features.get_non_alfanum(word),
                                word_features.get_trigram_freq(word, data_set.tri_freq),
                                word_features.get_word_frequency(word, data_set.word_freq),
                                word_features.contains_vowel(word),
                                word_features.word_length(word),
                                word_features.get_num_upper(word),
                                word_features.has_numbers(word)])

    classified_words = word_classifier.predict(feature_vectors, svm_model)

    if c.verbose:
        print(classified_words)

    corrected_text = []
    for word, classification in classified_words:
        if classification == 0:
            corrected_word = error_correction.split_error_correction(word, data_set.word_freq, conf)
        else:
            corrected_word = word

        if c.verbose:
            print("Replaced %s with %s" % (word, corrected_word))

        if isinstance(corrected_word, list):
            corrected_text.extend(corrected_word)
        else:
            corrected_text.append(corrected_word)

    return corrected_text


def clean_run():
    if os.path.exists(c.svm_model):
        os.remove(c.svm_model)

    if os.path.exists(c.main_db):
        os.remove(c.main_db)

    if os.path.exists(c.input):
        os.remove(c.input)

    if os.path.exists(c.training_data):
        os.remove(c.training_data)

    if os.path.exists(c.word_freq_path):
        os.remove(c.word_freq_path)

    if os.path.exists(c.trigrams_path):
        os.remove(c.trigrams_path)


def post_processing_file(input_file, output_file=False):
    sample_size = 0

    if not h.is_non_zero_file(input_file):
        print("Input file is empty or do not exsist.")
        return

    if '-c' in sys.argv:
        clean_run()
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

    conf = Configuration(number_of_vectors_from_each_source,
                         size_training_data,
                         svm_kernal,
                         c_value,
                         gamma,
                         max_words,
                         max_trigrams,
                         max_edit_distance,
                         min_edit_distance,
                         sample_size)

    data = DataSet(conf)
    svm_model, performace_report = word_classifier.train(conf)

    corrected_text = process_file(input_file, svm_model, data, conf)

    if output_file:
        with open(output_file, 'w') as fd:
            for word in corrected_text:
                fd.write("%s " % word)
    else:
        print(' '.join(corrected_text))


def main():
    sample_size = 0

    if '-c' in sys.argv:
        clean_run()
    if '-ss' in sys.argv:
        sample_size = 1
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
    min_edit_distance = 1

    h.build_file_structure()
    conf = Configuration(number_of_vectors_from_each_source,
                         size_training_data,
                         svm_kernal,
                         c_value,
                         gamma,
                         max_words,
                         max_trigrams,
                         max_edit_distance,
                         min_edit_distance,
                         sample_size)

    data = DataSet(conf)
    svm_model, performace_report = word_classifier.train(conf)

    print("Correcting text (1/6)")
    process_dir(c.ocr_output_OcropusArgus, c.output_OcropusArgus, svm_model, data, conf)
    print("Correcting text (2/6)")
    process_dir(c.ocr_output_OcropusGrepect, c.output_OcropusGrepect, svm_model, data, conf)
    print("Correcting text (3/6)")
    process_dir(c.ocr_output_TesseractArgus, c.output_TesseractArgus, svm_model, data, conf)
    print("Correcting text (4/6)")
    process_dir(c.ocr_output_TesseractGrepect, c.output_TesseractGrepect, svm_model, data, conf)
    print("Correcting text (5/6)")
    process_dir(c.ocr_output_ABBYYGrepect, c.output_ABBYYGrepect, svm_model, data, conf)
    print("Correcting text (6/6)")
    process_dir(c.ocr_output_ABBYYArgus, c.output_ABBYYArgus, svm_model, data, conf)

    conf.make_conf_file(performace_report)
    accuracyScript.combined_accuracy_report()


class Configuration():
    def __init__(self, number_of_vectors_from_each_source,
                 size_training_data,
                 svm_kernal,
                 c_value,
                 gamma,
                 max_words,
                 max_trigrams,
                 max_edit_distance,
                 min_edit_distance,
                 sample_size):
        self.number_of_vectors_from_each_source = number_of_vectors_from_each_source
        self.size_training_data = size_training_data
        self.svm_kernal = svm_kernal
        self.c_value = c_value
        self.gamma = gamma
        self.max_words = max_words
        self.max_trigrams = max_trigrams
        self.max_edit_distance = max_edit_distance
        self.min_edit_distance = min_edit_distance
        self.sample_size = sample_size

    def make_conf_file(self, svm_performance_report):
        output_array = []
        output_array.append("Parameters:\n")
        output_array.append("Number of vectors from each source=%s\n" % self.number_of_vectors_from_each_source)
        output_array.append("SVM parameters:\n\t Kernel: %s\n\t Gamma: %s\n\t C-value: %s\n\t Training data size: %s\n"
                           % (self.svm_kernal, self.gamma, self.c_value, self.size_training_data))
        output_array.append("SVM Performace:\n")
        output_array.append(svm_performance_report)
        output_array.append("Total number of words/freq in dataset: %s\n" % self.max_words)
        output_array.append("Total number of tri-grams/freq in dataset: %s\n" % self.max_trigrams)
        output_array.append("Max edit distance: %s\n" % self.max_edit_distance)
        output_array.append("Min edit distance: %s\n" % self.min_edit_distance)
        output_array.append("Number of pages from each source processed (0 means all pages): %s" % self.sample_size)

        with open(os.path.join(c.working_folder, "configuration.txt"), 'w') as fd:
            for line in output_array:
                fd.write(line)


class DataSet():
    tri_freq = {}
    word_freq = {}
    training_data = []

    def __init__(self, configuration):
        self.configuration = configuration
        self.tri_freq, self.word_freq, self.training_data = build_data_structure.build_data(configuration.max_trigrams,
                                                                                            configuration.max_words,
                                                                                            configuration.number_of_vectors_from_each_source)
main()

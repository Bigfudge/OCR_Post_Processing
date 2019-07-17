import helper_funtions as h
import constants as c
import os
import subprocess


def evaluate_file(ocr_file, truth_file):
    if not h.is_non_zero_file(ocr_file) or not h.is_non_zero_file(truth_file):
        print("Empty file: %s or %s" % (ocr_file, truth_file))
        return 0, 0

    cmd_word_accuracy = ["java", "-jar", c.primaPath, "-gt-text", truth_file, "-res-text", ocr_file,
                         "-method", "WordAccuracy"]
    cmd_caller = subprocess.Popen(cmd_word_accuracy, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_string_word_acc, error = cmd_caller.communicate()

    cmd_char_accuracy = ["java", "-jar", c.primaPath, "-gt-text", truth_file, "-res-text", ocr_file,
                         "-method", "CharacterAccuracy"]
    cmd_caller = subprocess.Popen(cmd_char_accuracy, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_string_char_acc, error = cmd_caller.communicate()

    word_accuracy = _get_word_accuracy_from_output_string(output_string_word_acc)
    character_accuracy = _get_char_accuracy_from_output_string(output_string_char_acc)

    if c.verbose:
        print("%s \t WordAccuracy: %f \t CharacterAccuracy: %f \n" % (ocr_file, word_accuracy, character_accuracy))

    return word_accuracy, character_accuracy


def evaluate_dir(ocr_output_path, ground_truth_path, source):
    pair_of_paths = h.get_pair(ocr_output_path, ground_truth_path, source)
    number_of_files = len(pair_of_paths)
    avg_word_acc = 0
    avg_char_acc = 0
    count = 0

    for ocr_file, truth_file in pair_of_paths:
        ocr_path = os.path.join(ocr_output_path, ocr_file)
        truth_path = os.path.join(ground_truth_path, truth_file)

        word_accuracy, character_accuracy = evaluate_file(ocr_path, truth_path)

        avg_word_acc += word_accuracy / number_of_files
        avg_char_acc += character_accuracy / number_of_files

        if c.verbose:
            count += 1
            print("Evaluated file: %i/%i" % (count, number_of_files))

    if c.verbose:
        print("Average:\t WordAccuracy: %f \t CharacterAccuracy: %f \n" % (avg_word_acc, avg_char_acc))

    return avg_word_acc, avg_char_acc


def _get_word_accuracy_from_output_string(output_string):
    acc = str(output_string).split(',')[2][1:-1]
    return float(acc)


def _get_char_accuracy_from_output_string(output_string):
    acc = str(output_string).split(',')[2][1:-5]
    return float(acc)

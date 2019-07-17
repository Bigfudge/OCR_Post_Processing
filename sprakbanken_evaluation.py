import constants as c
import helper_funtions as h
import sb_evaluation
import os

def evaluate_file(ocr_file, truth_file):
    if(not h.is_non_zero_file(ocr_file) or not h.is_non_zero_file(truth_file)):
        print("Empty file: %s or %s" % (ocr_file, truth_file))
        return 0,0

    character_errorrate, word_errorrate = sb_evaluation.main("-sb", [[ocr_file, truth_file]])

    if(c.verbose):
        print("%s \t Word Errorrate: %f \t Character Errorrate: %f \n"%(ocr_file, character_errorrate, word_errorrate))

    return 100*word_errorrate, 100*character_errorrate

def evaluate_dir(ocr_output_path, ground_truth_path, source):
    pairOfPaths= h.get_pair(ocr_output_path, ground_truth_path, source)
    avg_Word_Acc=0
    avg_Char_Acc=0
    count=0
    pairOfPaths = [[os.path.join(ocr_output_path, pair[0]), os.path.join(ground_truth_path, pair[1])]for pair in pairOfPaths]

    character_errorrate, word_errorrate = sb_evaluation.main("-sb", pairOfPaths)

    if(c.verbose):
        print("Word Errorrate: %f \t Character Errorrate: %f \n"%(character_errorrate, word_errorrate))

    return 100*word_errorrate, 100*character_errorrate
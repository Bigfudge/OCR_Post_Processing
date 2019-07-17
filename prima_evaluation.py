import helper_funtions as h
import constants as c
import os
import subprocess

def evaluate_file(ocr_file, truth_file):
    if(not h.is_non_zero_file(ocr_file) or not h.is_non_zero_file(truth_file)):
        print("Empty file: %s or %s" % (ocr_file, truth_file))
        return 0,0

    cmd_Word_Accuracy = ["java","-jar",c.primaPath,"-gt-text",truth_file,"-res-text",ocr_file,
            "-method", "WordAccuracy"]
    cmd_caller = subprocess.Popen(cmd_Word_Accuracy, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_string_WordAcc, error = cmd_caller.communicate()

    cmd_Char_Accuracy = ["java","-jar",c.primaPath,"-gt-text",truth_file,"-res-text",ocr_file,
            "-method", "CharacterAccuracy"]
    cmd_caller = subprocess.Popen(cmd_Char_Accuracy, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_string_CharAcc, error = cmd_caller.communicate()

    word_accuracy= _get_Word_Accuracy_from_output_string(output_string_WordAcc)
    character_accuracy= _get_Char_Accuracy_from_output_string(output_string_CharAcc)

    if(c.verbose):
        print("%s \t WordAccuracy: %f \t CharacterAccuracy: %f \n"%(ocr_file,word_accuracy,character_accuracy))

    return word_accuracy, character_accuracy

def evaluate_dir(ocr_output_path, ground_truth_path, source):
    pairOfPaths= h.get_pair(ocr_output_path, ground_truth_path, source)
    number_of_files=len(pairOfPaths)
    avg_Word_Acc=0
    avg_Char_Acc=0
    count=0


    for	ocr_file, truth_file in pairOfPaths:
        ocr_path = os.path.join(ocr_output_path, ocr_file)
        truth_path = os.path.join(ground_truth_path, truth_file)

        word_accuracy, character_accuracy = evaluate_file(ocr_path, truth_path)

        avg_Word_Acc += word_accuracy/number_of_files
        avg_Char_Acc += character_accuracy/number_of_files

        if(c.verbose):
            count+=1
            print("Evaluated file: %i/%i"%(count,number_of_files))

    if(c.verbose):
        print("Average:\t WordAccuracy: %f \t CharacterAccuracy: %f \n"%(avg_Word_Acc, avg_Char_Acc))

    return avg_Word_Acc, avg_Char_Acc

def _get_Word_Accuracy_from_output_string(output_string):
    acc=str(output_string).split(',')[2][1:-1]
    return float(acc)

def _get_Char_Accuracy_from_output_string(output_string):
    acc=str(output_string).split(',')[2][1:-5]
    return float(acc)

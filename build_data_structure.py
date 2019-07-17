#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import csv
import os
import glob
import align
import uuid
import collections
import sqlite3
import constants as c
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import math
import pickle
import accuracyScript
import helper_funtions as h
import word_features
from nltk.util import ngrams


def generate_valid_word_features(input_dir, max_size_output,tri_gram_dict,word_freq):
    output=[]

    for file in os.listdir(input_dir):
        truth = open(input_dir+file)
        words = [word for line in truth for word in line.split()]
        for word in words:
            word=h.filter_word(word)
            if(word):
                output.append([
                            h.remove_tags(word),
                            word_features.get_non_alfanum(word),
                            word_features.get_trigram_freq(word, tri_gram_dict),
                            word_features.get_word_frequency(word, word_freq),
                            word_features.contains_vowel(word),
                            word_features.word_length(word),
                            word_features.get_num_upper(word),
                            word_features.has_numbers(word),
                            1])
                if(max_size_output):
                    if(max_size_output<len(output)):
                        return output
    return output

def generate_error_word_features(ocr_dir,truth_dir, max_size_output,tri_gram_dict,word_freq, error_words, source):
    output=[]
    words = get_error_words(error_words, ocr_dir, truth_dir, source)

    for word in words:
        word=h.filter_word(word)
        if(word):
            output.append([
                        word,
                        word_features.get_non_alfanum(word),
                        word_features.get_trigram_freq(word,tri_gram_dict),
                        word_features.get_word_frequency(word, word_freq),
                        word_features.contains_vowel(word),
                        word_features.word_length(word),
                        word_features.get_num_upper(word),
                        word_features.has_numbers(word),
                        0])

            if(max_size_output):
                if(max_size_output<len(output)):
                    return output
    return output


#Generates a sorted dict of the most frequent tri-grams
def generate_trigram_freq_dict(max_size_output, words):
    input_files=[]
    if(not os.path.isfile(c.trigrams_path)):
        tri_grams = []
        sortedOutput={}

        tri_grams.extend(h.generate_trigram(words))
        output=calc_freq_from_list(tri_grams)

        for key, value in sorted(output.items(), key=lambda item: item[1], reverse=True):
            if(len(sortedOutput) >= max_size_output):
                break
            sortedOutput[key]=value

        h.save_obj(sortedOutput, "tri_gram")
    else:
        sortedOutput=h.load_obj("tri_gram")

    return(sortedOutput)

#Generates sorted dict of the most frequent words
def generate_word_freq_dict(max_size_output, words):
    if(not os.path.isfile(c.word_freq_path)):
        sortedOutput={}

        word_freqs=calc_freq_from_list(words)

        for key, value in sorted(word_freqs.items(), key=lambda item: item[1], reverse=True):
            if(len(sortedOutput)>=max_size_output):
                break
            sortedOutput[key]=value

        h.save_obj(sortedOutput, "word_freq")
    else:
        sortedOutput=h.load_obj("word_freq")

    return(sortedOutput)

#Extracts all words from the files in the data folder
def get_all_words():
    all_words=[]
    input_files=get_all_files_recursively(c.data_filepath)

    for file_name in input_files:
        all_words.extend(h.get_txt_from_file(file_name))
        filtered_words=h.filter_text(all_words)

    return filtered_words

def get_all_files_recursively(root_dir):
    all_files=[]
    for filename in glob.iglob(root_dir + '**/*', recursive=True):
        if os.path.isfile(filename):
            all_files.append(filename)
    return all_files

def calc_freq_from_list(input_list):
    output={}
    for item in input_list:
        if(item not in output):
            output[item]=1
        else:
            output[item]+=1
    return output

#Extracts all the error words from the files in ocr_dir given corresponding GS-files in truth_dir
def get_error_words(error_words, ocr_dir, truth_dir, source):
    ocr_dirs=[]
    truth_dirs=[]

    if(not os.path.isfile("models/"+error_words+".pkl")):
        pairs=h.get_pair(ocr_dir, truth_dir, source)
        
        for ocr_file, truth_file in pairs:
            ocr_dirs.append(ocr_dir+ocr_file)
            truth_dirs.append(truth_dir+truth_file)

        #Uses a modified version of språkbankens evaluation-script to extract the erronous words.
        words=align.main("-sb",ocr_dirs,truth_dirs, error_words)
        h.save_obj(words, error_words)
    else:
        words=h.load_obj(error_words)
    return words

def build_data(max_trigrams, max_words, number_of_vectors_from_each_source):
    words=[]
    if(not os.path.isfile(c.word_freq_path) and not os.path.isfile(c.trigrams_path)):
        words=get_all_words()

    tri_freq = generate_trigram_freq_dict(max_trigrams, words)
    word_freq = generate_word_freq_dict(max_words, words)
    training_data = get_training_data(number_of_vectors_from_each_source,tri_freq,word_freq)

    return  tri_freq, word_freq, training_data

def get_training_data(number_of_vectors_from_each_source,tri_freq,word_freq):
    training_data=[]

    #Generates the training data for each source of text
    if(not os.path.isfile(c.training_data)):
        training_data.extend(generate_valid_word_features(c.truthArgus, number_of_vectors_from_each_source, tri_freq, word_freq))
        print("Added words (1/10)")
        training_data.extend(generate_valid_word_features(c.truthGrepect, number_of_vectors_from_each_source, tri_freq, word_freq))
        print("Added words (2/10)")
        training_data.extend(generate_valid_word_features(c.truthArgus, number_of_vectors_from_each_source, tri_freq, word_freq))
        print("Added words (3/10)")
        training_data.extend(generate_valid_word_features(c.truthGrepect, number_of_vectors_from_each_source, tri_freq, word_freq))
        print("Added words (4/10)")
        training_data.extend(generate_error_word_features(c.ocr_output_OcropusArgus, c.truthArgus, number_of_vectors_from_each_source, tri_freq,word_freq, c.error_words_OcropusArgus, 'Argus'))
        print("Added words (5/10)")
        training_data.extend(generate_error_word_features(c.ocr_output_OcropusGrepect, c.truthGrepect, number_of_vectors_from_each_source, tri_freq,word_freq, c.error_words_OcropusGrepect, 'Grepect'))
        print("Added words (6/10)")
        training_data.extend(generate_error_word_features(c.ocr_output_TesseractArgus, c.truthArgus, number_of_vectors_from_each_source, tri_freq,word_freq, c.error_words_TesseractArgus, 'Argus'))
        print("Added words (7/10)")
        training_data.extend(generate_error_word_features(c.ocr_output_TesseractGrepect, c.truthGrepect, number_of_vectors_from_each_source, tri_freq, word_freq, c.error_words_TesseractGrepect, 'Grepect'))
        print("Added words (8/10)")
        training_data.extend(generate_error_word_features(c.ocr_output_ABBYYArgus, c.truthArgus, number_of_vectors_from_each_source, tri_freq, word_freq, c.error_words_ABBYYArgus, 'Argus'))
        print("Added words (9/10)")
        training_data.extend(generate_error_word_features(c.ocr_output_ABBYYGrepect, c.truthGrepect, number_of_vectors_from_each_source, tri_freq, word_freq, c.error_words_ABBYYGrepect, 'Grepect'))
        print("Added words (10/10)")

        h.save_obj(training_data, "training_data")
    else:
        sortedOutput=h.load_obj("training_data")

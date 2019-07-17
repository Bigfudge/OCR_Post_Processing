import os
import constants as c
import helper_funtions as h
import nltk
from nltk.util import ngrams

############### CALCULATES METRIC FOR SINGLE WORD ###############
def get_non_alfanum(word):
    errors = list(filter(lambda a: not (a.isalnum() | (a in {'å','ä','ö'})), word))
    return len(errors)

def get_word_frequency(word, freq_dict):
    if(word in freq_dict):
        return int(freq_dict[word])/len(freq_dict)
    return 0

def get_trigram_freq(word, tri_gram_dict):
    output=1
    chrs = [c for c in word]
    trigrams= ngrams(chrs,3)
    for gram in trigrams:
        if(gram in tri_gram_dict):
            output*=tri_gram_dict[gram]/len(tri_gram_dict)
        else:
            output*=0.001
    return output

def get_pentagram_freq(context, penta_gram_dict):
    if(tuple(context) in penta_gram_dict):
        print(freq[1]/len(freq))
        print("PENTA")
        return freq[1]/len(freq)
    else:
        return 0

def word_length(word):
    return(len(word)>13)

def get_num_upper(word):
    count=0
    for char in word:
        if(char.isupper()):
            count+=1
    return count

def contains_vowel(word):
    vowels = {"a", "e", "i", "o", "u","å","ä", "ö", "A", "E", "I", "O", "U","Å", "Ä", "Ö"}
    return any(char in vowels for char in word)

def has_numbers(word):
    count=0
    for char in word:
        if(char.isdigit()):
            count+=1
    return count

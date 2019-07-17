import pickle
import glob
import xml.etree.ElementTree as ET
from nltk.util import ngrams
import re
import os
import constants as c
import datetime

#Returns the number of non-alpha characters in a word
def get_non_alfa(word):
    errors = list(filter(lambda a: not (a.isalpha() | (a in {'å','ä','ö'})), word))
    return len(errors)

#Removes everything between tag-symbols (<>)
def remove_tags(word):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', word)
  return cleantext

#Save a given object to the model folder
def save_obj(obj, name ):
    with open('models/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

#Loads a object from models folder
def load_obj(name ):
    with open('models/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

#Applies the filters to the words. If the word should be removed, false is returned
def filter_word(word):
    #Removes all empty words
    if len(word)==0:
        return False
    #Removes the word if it is only non-alpha characters(Only non-alpha filter)
    if(get_non_alfa(word)==len(word)):
        return False
    #Removes the last character if it is a punctionation(Last char filter)
    if(word[-1] in {'.',',','!','?',':',';','\'','"','-','/'}):
        word= word[:-1]
    #Removes any one-character words that is not in the "dictionary"
    if(len(word)<=1 and word.lower() not in ["i", "å", "ö", "l", "e", "à"]):
        return False

    return word

#Applies the filters for a list of words. Returnes a list of the filtered words
def filter_text(words):
    filtered_words=[]
    for word in words:
        word = filter_word(word)
        if(word):
            filtered_words.append(word)
    return filtered_words

#Removes and prints all files in a path
def remove_output(path):
    files = glob.glob(path)
    for f in files:
        print(f)
        os.remove(f)

#Generates a list of trigrams given a list of words.
def generate_trigram(words):
    tri_grams=[]
    characters = [c for c in words]
    trigrams= ngrams(characters,3)
    for gram in trigrams:
        tri_grams.append(tuple(gram))
    return tri_grams

#Extract all words from a .xml file
def extract_words_xml(xml_file):
    all_words=[]
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for text in root:
        for paragraph in text:
            for sentence in paragraph:
                for word in sentence:
                    all_words.append(str(word.text))
    return(all_words)

def is_non_zero_file(fpath):
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False

#Extract the words from a file with file-ending .xml or .txt
def get_txt_from_file(file_path):
    if file_path.endswith('.xml'):
        words = extract_words_xml(file_path)
    elif(file_path.endswith('.txt')):
        text = open(file_path, 'r')
        words = [word for line in text for word in line.split()]
    return words


def get_pair(ocr_output_folder, ground_truth_folder, source):
    pairOfPaths= []
    for ocr_file in os.listdir(ocr_output_folder):
        for truth_file in os.listdir(ground_truth_folder):
            ocr_file_name_without_file_ending = os.path.splitext(ocr_file)[0]
            ground_truth_without_file_ending = os.path.splitext(truth_file)[0]

            if(source == "Grepect"):
                if(ocr_file_name_without_file_ending==ground_truth_without_file_ending):
                    pairOfPaths.append([ocr_file,truth_file])
            elif(source=="Argus"):
                if(ocr_file_name_without_file_ending[-4:]==ground_truth_without_file_ending[-4:]):
                    pairOfPaths.append([ocr_file,truth_file])
            else:
                print("Wrong engine")
                return []

    return pairOfPaths

def update_output_constants():
    c.output_OcropusArgus=c.working_folder+c.output_OcropusArgus
    c.output_OcropusGrepect=c.working_folder+c.output_OcropusGrepect
    c.output_TesseractArgus=c.working_folder+c.output_TesseractArgus
    c.output_TesseractGrepect=c.working_folder+c.output_TesseractGrepect
    c.output_ABBYYArgus=c.working_folder+c.output_ABBYYArgus
    c.output_ABBYYGrepect=c.working_folder+c.output_ABBYYGrepect
    c.output_filepath=c.working_folder+c.output_filepath


def build_file_structure():

    now = datetime.datetime.now()
    folder_name= now.strftime("%Y-%m-%d %H:%M")
    folder_path=os.path.join("./Evaluation-reports",folder_name)
    os.mkdir(folder_path)
    c.working_folder=folder_path
    update_output_constants()

    if(not os.path.exists(c.data_filepath)):
        os.mkdir(c.data_filepath)
    if(not os.path.exists(c.models_filepath)):
        os.mkdir(c.models_filepath)
    if(not os.path.exists(c.output_filepath)):
        os.mkdir(c.output_filepath)
    if(not os.path.exists(c.output_OcropusArgus)):
        os.mkdir(c.output_OcropusArgus)
    if(not os.path.exists(c.output_OcropusGrepect)):
        os.mkdir(c.output_OcropusGrepect)
    if(not os.path.exists(c.output_TesseractArgus)):
        os.mkdir(c.output_TesseractArgus)
    if(not os.path.exists(c.output_TesseractGrepect)):
        os.mkdir(c.output_TesseractGrepect)
    if(not os.path.exists(c.output_ABBYYArgus)):
        os.mkdir(c.output_ABBYYArgus)
    if(not os.path.exists(c.output_ABBYYGrepect)):
        os.mkdir(c.output_ABBYYGrepect)

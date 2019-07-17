import os
import re

def remove_tags(word):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', word)
  return cleantext

def lastCharNonAlfa(word):
    return (word[-1] in {'.',',','!','?',':',';','\'','"','-','/'})

def prune_data(input_dir):
    for file in os.listdir(input_dir):
        input = open(input_dir+"/"+file)
        output = remove_tags(input.read())
        f = open(input_dir+"/"+file, "w")
        f.write(output)

prune_data("./data/corpus/runeberg/")

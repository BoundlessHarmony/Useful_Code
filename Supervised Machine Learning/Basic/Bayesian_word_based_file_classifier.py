import numpy as np
import pandas as pd
from pathlib import Path
import os
import re

# ================================
# Define a function to retrieve all file paths recursively from a specified directory
def recurse_paths(directory):
    """
    Retrieve all file paths from the given directory recursively.
    """
    path = Path(directory)
    return [str(file) for file in path.rglob('*') if file.is_file()]

# Generalized paths for good and bad directories
good_path = "<your_good_files_directory>"  # Replace with the path to good files
bad_path = "<your_bad_files_directory>"    # Replace with the path to bad files

# Retrieve lists of all good and bad files for classification
good_files = recurse_paths(good_path)
bad_files = recurse_paths(bad_path)

print(f'Total good files: {len(good_files)}')
print(f'Total bad files: {len(bad_files)}')

# ================================
# Define a function to extract words from a file
def get_words(file_name):
    """
    Retrieve all words from the file content, removing headers and non-alphanumeric characters.
    """
    regex = re.compile("[^\w\s]")
    words = list()
    with open(file_name, encoding='utf8', errors='ignore') as f:
        text = f.readlines()
        finished_header = False
        for line in text:
            line = line.lower()
            if finished_header:
                for word in re.sub(regex, '', line).split():
                    words.append(word)
            elif line == "\n":
                finished_header = True
    return words

# Collect unique words from all good and bad files
good_words = set()
bad_words = set()
for file in good_files:
    for word in get_words(file):
        good_words.add(word)

for file in bad_files:
    for word in get_words(file):
        bad_words.add(word)

# ================================
# Define a function to classify files based on word presence
def classify_file(filename):
    """
    Classify a file as good or bad based on word presence in predefined sets.
    """
    words = get_words(filename)
    num_words = len(words)
    set_words = set(words)
    num_good = len([True for word in set_words if word in good_words])
    num_bad = len([True for word in set_words if word in bad_words])
    return (num_words, num_good, num_bad)

# Classify a set of files and calculate accuracy for good files
good_classification = []
for file in good_files:
    results = classify_file(file)
    good_classification.append(True if results[1] > results[2] else False)
good_accuracy = (len(np.array(good_classification)[np.where(good_classification)]) / len(good_classification)) * 100.0
print(f'Good Classification Accuracy: {good_accuracy}')

# Classify a set of files and calculate accuracy for bad files
bad_classification = []
for file in bad_files:
    results = classify_file(file)
    bad_classification.append(True if results[1] < results[2] else False)
bad_accuracy = (len(np.array(bad_classification)[np.where(~np.array(bad_classification))]) / len(bad_classification)) * 100.0
print(f'Bad Classification Accuracy: {bad_accuracy}')

# ================================
# Calculate word frequencies for good and bad words
bad_word_frequency = {}
for file in bad_files:
    words = set(get_words(file))
    for word in words:
        bad_word_frequency[word] = bad_word_frequency.get(word, 0) + 1

good_word_frequency = {}
for file in good_files:
    words = set(get_words(file))
    for word in words:
        good_word_frequency[word] = good_word_frequency.get(word, 0) + 1

# ================================
# Calculate probabilities for word classification based on frequencies
def bad_word_probability(words):
    """
    Calculate probability of each word being in a bad file.
    """
    bad_prob_dict = {}
    total_bad_files = len(bad_files)
    for word in set(words):
        word_freq = bad_word_frequency.get(word, 0)
        bad_prob = (word_freq + 1) / (total_bad_files + 2)
        bad_prob_dict[word] = bad_prob
    return bad_prob_dict

def good_word_probability(words):
    """
    Calculate probability of each word being in a good file.
    """
    good_prob_dict = {}
    total_good_files = len(good_files)
    for word in set(words):
        word_freq = good_word_frequency.get(word, 0)
        good_prob = (word_freq + 1) / (total_good_files + 2)
        good_prob_dict[word] = good_prob
    return good_prob_dict

# ================================
# Perform classification based on word probabilities
def classify_text(words):
    """
    Classify text as good or bad based on word probabilities.
    """
    good_prob = np.array([v for v in good_word_probability(words).values()]).prod()
    bad_prob = np.array([v for v in bad_word_probability(words).values()]).prod()
    classification = True if good_prob > bad_prob else False
    return classification, good_prob, bad_prob

# Classify a set of good files and calculate accuracy based on probabilities
good_results = []
for file in good_files:
    results = classify_text(get_words(file))
    good_results.append(results[0])
good_accuracy = (len(np.array(good_results)[np.where(good_results)]) / len(good_results)) * 100.0
print(f'Good Probability-Based Classification Accuracy: {good_accuracy}')

# Classify a set of bad files and calculate accuracy based on probabilities
bad_results = []
for file in bad_files:
    results = classify_text(get_words(file))
    bad_results.append(results[0])
bad_accuracy = (len(np.array(bad_results)[np.where(~np.array(bad_results))]) / len(bad_results)) * 100.0
print(f'Bad Probability-Based Classification Accuracy: {bad_accuracy}')

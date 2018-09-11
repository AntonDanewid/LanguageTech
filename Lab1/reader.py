#!/usr/bin/python
import os
import regex as re
import pickle


def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    :param dir:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files


index = {}


def find_all_occurences(wordCandidate, files):
    p = re.compile('[a-ö]+')
    if p.match(wordCandidate) is None:
        return
    # print(p.match(wordCandidate).group())
    word = p.match(wordCandidate).group()
    if word in index:
        return
    file_dictionary = {}
    for file in files:
        li = list()
        pattern = "\\b" + word + "\\b"
        regex = re.compile(pattern, re.IGNORECASE)
        open_file = open(file, "r", encoding='utf-8')
        text = open_file.read()
        for m in regex.finditer(text):
            li.append(m.start())
        if len(li) is not 0:
            file_dictionary[open_file.name] = li
    index[word] = file_dictionary


def main():
    files = get_files(".", "txt")
    for file in files:
        print(file)
        open_file = open(file, "r", encoding='utf-8')
        for line in open_file:
            words = line.split()
            for word in words:
                # print(index)
                find_all_occurences(word.lower(), files)
    print(index)
    pickle.dump(index, open("save.p", "wb"))


if __name__ == "__main__":
    main()

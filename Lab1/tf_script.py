import pickle
import os
import math
import regex as re

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


def load_tf(index, word, document):
    positions = index[word]
    if document not in positions.keys():
        return 0
    tf = len(positions[document]) / wordCount[document]
    idf = math.log(len(files) / (len(positions.keys())), 10)

    return_dict = {}
    return_dict[word] = tf * idf
    return tf * idf


def calc_cosine_similarity(document1, document2):
    sum = 0
    length1 = 0
    length2 = 0
    for word in document1:
        sum = sum + (document1[word] * document2[word])
        length1 = length1 + (document1[word] * document1[word])
        length2 = length2 + (document2[word] * document2[word])
    length1 = math.sqrt(length1)
    length2 = math.sqrt(length2)
    return sum / (length1*length2)




def tokenize(text):
    words = re.findall('\p{L}+', text)
    return len(words)


files = get_files(".", "txt")
wordCount = {}
for file in files:
    wordCount[file] = tokenize(open(file, "r", encoding='utf-8').read())


def main():
    index = pickle.load(open("save.p", "rb"))
    filedict = {}
    for file in files:
        array = {}
        for word in index.keys():
            array[word] = load_tf(index, word, file)
        filedict[file] = array
    print(filedict)
    # print(len(index["nils"]["nils.txt"]))
    # print(filedict["jerusalem.txt"]["nils"])
    print(index["samlar"])
    print(filedict["nils.txt"]["nils"])
    for doc1 in filedict.keys():
        for doc2 in filedict.keys():
            print("The cosine between ", doc1, " and ", doc2, " ", calc_cosine_similarity(filedict[doc1], filedict[doc2]))


#kjejsaren och troll
if __name__ == "__main__":
    main()
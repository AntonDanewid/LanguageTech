"""
CoNLL-X and CoNLL-U file readers and writers
"""
__author__ = "Pierre Nugues"

import os
import operator


def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    Recursive version
    :param dir:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        path = dir + '/' + file
        if os.path.isdir(path):
            files += get_files(path, suffix)
        elif os.path.isfile(path) and file.endswith(suffix):
            files.append(path)
    return files


def read_sentences(file):
    """
    Creates a list of sentences from the corpus
    Each sentence is a string
    :param file:
    :return:
    """
    print(file)
    f = open(file, encoding='utf-8').read().strip()
    sentences = f.split('\n\n')
    return sentences


def split_rows(sentences, column_names):
    """
    Creates a list of sentence where each sentence is a list of lines
    Each line is a dictionary of columns
    :param sentences:
    :param column_names:
    :return:
    """
    new_sentences = []
    root_values = ['0', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', '0', 'ROOT', '0', 'ROOT']
    start = [dict(zip(column_names, root_values))]
    for sentence in sentences:
        rows = sentence.split('\n')
        sentence = [dict(zip(column_names, row.split())) for row in rows if row[0] != '#']
        sentence = start + sentence
        new_sentences.append(sentence)
    return new_sentences



def verb_subject(data):
    numberOfSubjects = 0
    frequency = {}
    for line in data:
        # print(line)

        for dictionary in line:
            # print(dictionary["deprel"])
            if dictionary["deprel"] == "SS":
                numberOfSubjects = numberOfSubjects + 1
                subject = dictionary['form'].lower()
                head = int(dictionary['head'])
                line_head = line[head]
                verb = line[head]['form'].lower()
                if (verb, subject) in frequency:
                    frequency[verb, subject] = frequency[verb, subject] + 1
                else:
                    frequency[verb, subject] = 1
    sorted_x = sorted(frequency.items(), key=operator.itemgetter(1))
    # print(sorted_x)
    print(numberOfSubjects)


def verb_subject_object(data):
    frequency = {}
    count = 0
    for line in data:
        objectPos = []
        index = 0
        objectDict = {}
        for word in line:
            if word['deprel'] == 'OO':
                objectPos.append(index)
            index += 1

        # Get the verb that is associated with the OO
        # Key is object position, value is the deprel
        for pos in objectPos:
            objectDict[pos] = (line[pos])['head'].lower()
        for word in line:
            # If the word is a SS and the head(verb) has a outgoing edge to an OO
            if (word['deprel'] == 'SS' and word['head'] in objectDict.values()):
                #Find the outgoing edge to the OO
                for obj in objectDict:
                    if objectDict[obj] == word['head']:
                        count += 1
                        verbPos = int(word['head'])
                        verb = line[verbPos]['form'].lower()
                        subject = word['form'].lower()
                        objectParticle = line[obj]['form'].lower()
                        if (subject, verb, objectParticle) in frequency:
                            frequency[subject, verb, objectParticle] += 1
                        else:
                            frequency[subject, verb, objectParticle] = 1

    sorted_x = sorted(frequency.items(), key=operator.itemgetter(1), reverse=True)
    print(count)
    print(sorted_x)




def verb_subject_object_U(data):
    frequency = {}
    count = 0
    for line in data:
        objectPos = []
        index = 0
        objectDict = {}
        for word in line:
            if word['deprel'] == 'obj':
                objectPos.append(index)
            index += 1

        # Get the verb that is associated with the OO
        # Key is object position, value is the deprel
        for pos in objectPos:
            objectDict[pos] = (line[pos])['head'].lower()
        for word in line:
            # If the word is a SS and the head(verb) has a outgoing edge to an OO
            if (word['deprel'] == 'nsubj' and word['head'] in objectDict.values()):
                #Find the outgoing edge to the OO
                for obj in objectDict:
                    if objectDict[obj] == word['head']:
                        count += 1
                        verbPos = int(word['head'])
                        verb = line[verbPos]['form'].lower()
                        subject = word['form'].lower()
                        objectParticle = line[obj]['form'].lower()
                        if (subject, verb, objectParticle) in frequency:
                            frequency[subject, verb, objectParticle] += 1
                        else:
                            frequency[subject, verb, objectParticle] = 1

    sorted_x = sorted(frequency.items(), key=operator.itemgetter(1), reverse=True)
    print(count)
    print(sorted_x)








def save(file, formatted_corpus, column_names):
    f_out = open(file, 'w')
    for sentence in formatted_corpus:
        for row in sentence[1:]:
            # print(row, flush=True)
            for col in column_names[:-1]:
                if col in row:
                    f_out.write(row[col] + '\t')
                else:
                    f_out.write('_\t')
            col = column_names[-1]
            if col in row:
                f_out.write(row[col] + '\n')
            else:
                f_out.write('_\n')
        f_out.write('\n')
    f_out.close()


#Form är ordet, id är siffra relaterat till mening, deprel är typen. SS etc
if __name__ == '__main__':
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']

    train_file = 'swedish_talbanken05_train.conll'
    # train_file = 'test_x'
    test_file = 'swedish_talbanken05_test.conll'

    sentences = read_sentences(train_file)
    formatted_corpus = split_rows(sentences, column_names_2006)
    # print(train_file, len(formatted_corpus))
    # print(formatted_corpus[0])
    # verb_subject(formatted_corpus)
    # verb_subject_object(formatted_corpus)
    column_names_u = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc']
    files = get_files('ud-treebanks-v2.2/UD_Norwegian-Bokmaal', 'train.conllu')
    for train_file in files:
        sentences = read_sentences(train_file)
        formatted_corpus = split_rows(sentences, column_names_u)
        for sentence in formatted_corpus:
            for word in sentence:
                if '-' in word['id']:
                    sentence.remove(word)
        verb_subject_object_U(formatted_corpus)

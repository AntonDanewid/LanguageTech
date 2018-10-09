"""
Baseline chunker for CoNLL 2000
"""
__author__ = "Pierre Nugues"



"""
CoNLL 2000 file reader
"""
__author__ = "Pierre Nugues"


def read_sentences(file):
    """
    Creates a list of sentences from the corpus
    Each sen5tence is a string
    :param file:
    :return:
    """
    f = open(file).read().strip()
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
    for sentence in sentences:
        rows = sentence.split('\n')
        sentence = [dict(zip(column_names, row.split())) for row in rows]
        new_sentences.append(sentence)
    return new_sentences



def count_pos(corpus):
    """
    Computes the part-of-speech distribution
    in a CoNLL 2000 file
    :param corpus:
    :return:
    """
    pos_cnt = {}
    for sentence in corpus:
        for row in sentence:
            if row['pos'] in pos_cnt:
                pos_cnt[row['pos']] += 1
            else:
                pos_cnt[row['pos']] = 1
    return pos_cnt


def train(corpus):
    """
    Computes the chunk distribution by pos
    The result is stored in a dictionary
    :param corpus:
    :return:
    """
    pos_cnt = count_pos(corpus)
    # We compute the chunk distribution by POS
    chunk_dist = {key: {} for key in pos_cnt.keys()}
    """
    Fill in code to compute the chunk distribution for each part of speech
    """
    for line in corpus:
        for word in line:
            position = word['pos']
            chunk = word['chunk']
            try:
                chunk_dist[position][chunk] += 1
            except:
                chunk_dist[position] = {}
                chunk_dist[position][chunk] = 1


    # We determine the best association
    pos_chunk = {}
    """
    Fill in code so that for each part of speech, you select the most frequent chunk.
    You will build a dictionary with key values:
    pos_chunk[pos] = most frequent chunk for pos
    """
    for pos in chunk_dist:
        sortingInt = 0
        mostFrequentChunk = ""
        for chunk in chunk_dist[pos]:
            if chunk_dist[pos][chunk] > sortingInt:
                mostFrequentChunk = chunk
                sortingInt = chunk_dist[pos][chunk]
        pos_chunk[pos] = mostFrequentChunk

    print(pos_chunk)
    return pos_chunk


def predict(model, corpus):
    """
    Predicts the chunk from the part of speech
    Adds a pchunk column
    :param model:
    :param corpus:
    :return:
    """
    """
    We add a predicted chunk column: pchunk
    """
    for sentence in corpus:
        for row in sentence:
            row['pchunk'] = model[row['pos']]
    return corpus


def eval(predicted):
    """
    Evaluates the predicted chunk accuracy
    :param predicted:
    :return:
    """
    word_cnt = 0
    correct = 0
    for sentence in predicted:
        for row in sentence:
            word_cnt += 1
            if row['chunk'] == row['pchunk']:
                correct += 1
    return correct / word_cnt


if __name__ == '__main__':
    column_names = ['form', 'pos', 'chunk']
    train_file = 'train.txt'
    test_file = 'test.txt'

    train_corpus = read_sentences(train_file)
    train_corpus = split_rows(train_corpus, column_names)
    test_corpus = read_sentences(test_file)
    test_corpus = split_rows(test_corpus, column_names)

    model = train(train_corpus)

    predicted = predict(model, test_corpus)
    accuracy = eval(predicted)
    print("Accuracy", accuracy)
    f_out = open('out', 'w', newline = '\n')
    # We write the word (form), part of speech (pos),
    # gold-standard chunk (chunk), and predicted chunk (pchunk)
    for sentence in predicted:
        for row in sentence:
            f_out.write(row['form'] + ' ' + row['pos'] + ' ' +
                        row['chunk'] + ' ' + row['pchunk'] + '\n')
        f_out.write('\n')
    f_out.close()
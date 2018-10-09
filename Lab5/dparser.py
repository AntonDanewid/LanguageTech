"""
Gold standard parser
"""
__author__ = "Pierre Nugues"

import transition
import conll
import features
import sklearn
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn import preprocessing
from sklearn import linear_model
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib


def reference(stack, queue, graph):
    """
    Gold standard parsing
    Produces a sequence of transitions from a manually-annotated corpus:
    sh, re, ra.deprel, la.deprel
    :param stack: The stack
    :param queue: The input list
    :param graph: The set of relations already parsed
    :return: the transition and the grammatical function (deprel) in the
    form of transition.deprel
    """
    # Right arc
    if stack and stack[0]['id'] == queue[0]['head']:
        # print('ra', queue[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + queue[0]['deprel']
        stack, queue, graph = transition.right_arc(stack, queue, graph)
        return stack, queue, graph, 'ra' + deprel
    # Left arc
    if stack and queue[0]['id'] == stack[0]['head']:
        # print('la', stack[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + stack[0]['deprel']
        stack, queue, graph = transition.left_arc(stack, queue, graph)
        return stack, queue, graph, 'la' + deprel
    # Reduce
    if stack and transition.can_reduce(stack, graph):
        for word in stack:
            if (word['id'] == queue[0]['head'] or
                        word['head'] == queue[0]['id']):
                # print('re', stack[0]['cpostag'], queue[0]['cpostag'])
                stack, queue, graph = transition.reduce(stack, queue, graph)
                return stack, queue, graph, 're'
    # Shift
    # print('sh', [], queue[0]['cpostag'])
    stack, queue, graph = transition.shift(stack, queue, graph)
    return stack, queue, graph, 'sh'

def parse_ml(stack, queue, graph, trans):
    if stack and trans[:2] == 'ra' and transition.can_rightarc(stack):
        stack, queue, graph = transition.right_arc(stack, queue, graph, trans[3:])
        return stack, queue, graph, 'ra'
    elif stack and trans[:2] == 'la' and transition.can_leftarc(stack, graph):
        stack, queue, graph = transition.left_arc(stack, queue, graph, trans[3:])
        return stack, queue, graph, 'la'
    elif stack and trans[:2] == 're' and transition.can_reduce(stack, graph):
        stack, queue, graph = transition.reduce(stack, queue, graph)
        return stack, queue, graph, 're'
    elif stack and trans[:2] == 'sh':
        stack, queue, graph = transition.shift(stack, queue, graph)
        return stack, queue, graph, 'sh'
    else:
        stack, queue, graph = transition.shift(stack, queue, graph)
        return stack, queue, graph, 'sh'


def train_model():
    train_file = 'swedish_talbanken05_train.conll'
    test_file = 'swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

    sentences = conll.read_sentences(train_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)
    features1 = ['word_s0', 'pos_s0', 'word_q0', 'pos_q0', 'can_re', 'can_ra']
    features2 = ['word_s0', 'pos_s0', 'word_s1', 'pos_s1', 'word_q0', 'pos_q0', 'word_q1', 'pos_q1', 'can_re', 'can_ra']
    features3 = ['word_s0', 'pos_s0', 'word_s1', 'pos_s1', 'word_q0', 'pos_q0', 'word_q1', 'pos_q1', 'word_n0', 'pos_n0', 'word_n1', 'pos_n1', 'can_re', 'can_ra']



    sent_cnt = 0
    x_vect = []
    y_vect = []

    for sentence in formatted_corpus:
        sent_cnt += 1
        if sent_cnt % 1000 == 0:
            print(sent_cnt, 'sentences on', len(formatted_corpus), flush=True)
        stack = []
        queue = list(sentence)
        graph = {}
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'
        transitions = []
        while queue:
            feat = features.extract_3(stack, queue, graph, features3, sentence)
            stack, queue, graph, trans = reference(stack, queue, graph)
            transitions.append(trans)
            x_vect.append(feat)
            y_vect.append(trans)
            # print(feat, " = ", trans)
        stack, graph = transition.empty_stack(stack, graph)

        # Poorman's projectivization to have well-formed graphs.
        for word in sentence:
            word['head'] = graph['heads'][word['id']]
        # print(transitions)
        # print(graph)
    return x_vect, y_vect


def predict_sentence():
    train_file = 'swedish_talbanken05_train.conll'
    test_file = 'swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

    sentences = conll.read_sentences(test_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006_test)
    features1 = ['word_s0', 'pos_s0', 'word_q0', 'pos_q0', 'can_re', 'can_ra']
    features2 = ['word_s0', 'pos_s0', 'word_s1', 'pos_s1', 'word_q0', 'pos_q0', 'word_q1', 'pos_q1', 'can_re', 'can_ra']
    features3 = ['word_s0', 'pos_s0', 'word_s1', 'pos_s1', 'word_q0', 'pos_q0', 'word_q1', 'pos_q1', 'word_n0', 'pos_n0', 'word_n1', 'pos_n1', 'can_re', 'can_ra']

    sent_cnt = 0


    for sentence in formatted_corpus:
        sent_cnt += 1
        if sent_cnt % 1000 == 0:
            print(sent_cnt, 'sentences on', len(formatted_corpus), flush=True)
        stack = []
        queue = list(sentence)
        graph = {}
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'
        transitions = []
        while queue:

            feat = features.extract_3(stack, queue, graph, features3, sentence)
            # print(feat)
            feat = vec.transform(feat)
            trans_nr = model.predict(feat)
            # print(trans_nr)
            trans = label.inverse_transform(trans_nr)
            print(trans)
            # fel Graph
            stack, queue, graph, trans = parse_ml(stack, queue, graph, trans[0])

        stack, graph = transition.empty_stack(stack, graph)

        # Poorman's projectivization to have well-formed graphs.
        for word in sentence:
            word['head'] = graph['heads'][word['id']]
            word['deprel'] = graph['deprels'][word['id']]

    conll.save("test", formatted_corpus, column_names_2006)

if __name__ == '__main__':
    x_vec, y_vec = train_model()

    vec = DictVectorizer(sparse=True)
    X = vec.fit_transform(x_vec)
    label = preprocessing.LabelEncoder()
    Y = label.fit_transform(y_vec)
    # classifier = linear_model.LogisticRegression(penalty='l2', dual=True, solver='liblinear', verbose=True)
    # print(y_vec)
    print("Training model ")
    # model = classifier.fit(X, Y)
    print("Done training model  ")
    # joblib.dump(model, 'linearClassifier3.joblib')
    model = joblib.load('linearClassifier3.joblib')
    predict_sentence()



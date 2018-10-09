#    features1 = [ 'word_s0', 'pos_s0','word_q0', 'pos_q0', 'can_re','can_ra']


import transition


def extract(stack, queue, graph, feature_names, sentence):

    stack_list = ["nil", "nil"]
    if stack:
        stack_list[0] = stack[0]['form']
        stack_list[1] = stack[0]['postag']
    queue_list = ["nil", "nil"]
    if queue:
        queue_list[0] = queue[0]['form']
        queue_list[1] = queue[0]['postag']

    features = stack_list + queue_list
    can_re = transition.can_reduce(stack, graph)
    can_left_arc = transition.can_leftarc(stack, graph)
    features.append(can_re)
    features.append(can_left_arc)
    features = zip(feature_names, features)
    features = dict(features)
    # print(features)
    return features



def extract_2(stack, queue, graph, feature_names, sentence):

    stack_list = ["nil", "nil", "nil", "nil"]
    if stack:
        stack_list[0] = stack[0]['form']
        stack_list[1] = stack[0]['postag']
        if len(stack) > 1:
            stack_list[2] = stack[1]['form']
            stack_list[3] = stack[1]['postag']
    queue_list = ["nil", "nil", "nil", "nil"]
    if queue:
        queue_list[0] = queue[0]['form']
        queue_list[1] = queue[0]['postag']
        if len(queue) > 1:
            queue_list[2] = queue[1]['form']
            queue_list[3] = queue[1]['postag']
    features = stack_list + queue_list
    can_re = transition.can_reduce(stack, graph)
    can_left_arc = transition.can_leftarc(stack, graph)
    features.append(can_re)
    features.append(can_left_arc)
    features = zip(feature_names, features)
    features = dict(features)
    # print(features)
    return features



def extract_3(stack, queue, graph, feature_names, sentence):

    stack_list = ["nil", "nil", "nil", "nil"]
    if stack:
        stack_list[0] = stack[0]['form']
        stack_list[1] = stack[0]['postag']
        if len(stack) > 1:
            stack_list[2] = stack[1]['form']
            stack_list[3] = stack[1]['postag']
    queue_list = ["nil", "nil", "nil", "nil"]
    if queue:
        queue_list[0] = queue[0]['form']
        queue_list[1] = queue[0]['postag']
        if len(queue) > 1:
            queue_list[2] = queue[1]['form']
            queue_list[3] = queue[1]['postag']
    features = stack_list + queue_list

    previous_word = ["nil", "nil"]

    if stack:
        if int(stack[0]["id"]) > 0:
            word = sentence[int(stack[0]["id"]) -1]
            previous_word[0] = word['form']
            previous_word[1] = word['postag']

    features = features + previous_word

    next_word = ["nil", "nil"]
    if stack:
        if int(stack[0]["id"]) < len(sentence) - 1:
            word = sentence[int(stack[0]["id"]) + 1]
            next_word[0] = word['form']
            next_word[1] = word['postag']

    features = features + next_word




    can_re = transition.can_reduce(stack, graph)
    can_left_arc = transition.can_leftarc(stack, graph)
    features.append(can_re)
    features.append(can_left_arc)
    features = zip(feature_names, features)
    features = dict(features)
    # print(features)
    # print(features)
    return features

# extract_features(sentences, w_size, feature_names):
#     """
#     Builds X matrix and y vector
#     X is a list of dictionaries and y is a list
#     :param sentences:
#     :param w_size:
#     :return:
#     """

#     X_l = []
#     y_l = []
#     for sentence in sentences:
#         X, y = extract_features_sent(sentence, w_size, feature_names, False)
#         X_l.extend(X)
#         y_l.extend(y)
#     return X_l, y_l
#
#
# def extract_features_sent(sentence, w_size, feature_names, useChunk):
#     """
#     Extract the features from one sentence
#     returns X and y, where X is a list of dictionaries and
#     y is a list of symbols
#     :param sentence: string containing the CoNLL structure of a sentence
#     :param w_size:
#     :return:
#     """
#
#     # We pad the sentence to extract the context window more easily
#     start = "BOS BOS BOS\n"
#     end = "\nEOS EOS EOS"
#     start *= w_size
#     end *= w_size
#     sentence = start + sentence
#     sentence += end
#
#     # Each sentence is a list of rows
#     sentence = sentence.splitlines()
#     padded_sentence = list()
#     for line in sentence:
#         line = line.split()
#         padded_sentence.append(line)
#     # print(padded_sentence)
#
#     # We extract the features and the classes
#     # X contains is a list of features, where each feature vector is a dictionary
#     # y is the list of classes
#     X = list()
#     y = list()
#     for i in range(len(padded_sentence) - 2 * w_size):
#         # x is a row of X
#         x = list()
#         # The words in lower case
#         for j in range(2 * w_size + 1):
#             x.append(padded_sentence[i + j][0].lower())
#         # The POS
#         for j in range(2 * w_size + 1):
#             x.append(padded_sentence[i + j][1])
#         for j in range(w_size):
#             x.append(padded_sentence[i + j][2])
#             # for j in range(2):
#             #     x.append(padded_sentence[i - j + 1][2])
#         # The chunks (Up to the word)
#         """
#         for j in range(w_size):
#             feature_line.append(padded_sentence[i + j][2])
#         """
#         # We represent the feature vector as a dictionary
#         X.append(dict(zip(feature_names, x)))
#         # The classes are stored in a list
#         y.append(padded_sentence[i + w_size][2])
#     return X, y
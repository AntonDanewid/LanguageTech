import regex as re
import sys
import math


def normalize(text):
    text = re.sub(r'\n', r'', text)
    text = re.sub(r'\t', r'', text)
    text = re.sub(r',', r'', text)

    # print(text)
    sentences = re.findall(r'\p{Lu}+[^\.]+', text)
    sentences = ["<s> " + x.lower() + " </s>" for x in sentences]
    temp = " "
    for sentence in sentences:
        temp += sentence
        print(sentence)
    return temp


def tokenize(text):
    words = re.findall("<s>|</s>|\p{L}+", text)
    return words


def count_unigrams(words):
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency


def count_bigrams(words):
    bigrams = [tuple(words[inx:inx + 2])
               for inx in range(len(words) - 1)]

    frequency_bigrams = {}
    for bigram in bigrams:
        if bigram in frequency_bigrams:
            frequency_bigrams[bigram] += 1
        else:
            frequency_bigrams[bigram] = 1
    return frequency_bigrams


def calculate_entropy(probability, length):
    return -math.log(probability, 2) / length


if __name__ == '__main__':
    open_file = open("Selma.txt", "r", encoding='utf-8')
    normalized_text = normalize(open_file.read())

    open_file = open("Selma.txt", "r", encoding='utf-8')
    text = open_file.read()
    # number_of_words = len(tokenize(normalized_text))
    tokenized_normalized = tokenize(normalized_text)
    number_of_words = len(tokenized_normalized)
    frequency_unigrams = count_unigrams(tokenized_normalized)
    frequency_bigrams = count_bigrams(tokenized_normalized)

    targetSentence = "det var en gång en katt som hette nils </s>"
    probability = 1
    print("Unigram model")
    print("=====================================================")
    print("wi C(wi) #words P(wi)")
    print("=====================================================")
    targetWords = targetSentence.split()
    iterations = 0
    for word in targetWords: #re.finditer(r'\p{L}+|<s>|</s>', targetSentence):
        print(word,
              " ",
              frequency_unigrams[word],
              " ",
              number_of_words,
              " ",
              frequency_unigrams[word] / number_of_words)
        probability = probability * frequency_unigrams[word] / number_of_words
        iterations = iterations + 1
    print("=====================================================")
    print("Unigram probability for sentence ", probability)
    print("Geometric mean ",  probability**(1/float(iterations)))
    entropy = calculate_entropy(probability, len(tokenize(targetSentence)))
    print("Entropy rate: ", entropy)
    perplexity = math.pow(2, entropy)
    print("Perplexity: ", perplexity)
    print("\n\n\n")
    print("Bigram model")
    print("=====================================================")
    print("wi wi+1 Ci,i+1 C(i) P(wi+1|wi)")
    targetSentence = "<s> det var en gång en katt som hette nils </s>"
    targetWords = targetSentence.split()
    iterations = 1
    probability = 1
    for x in range(0, len(targetWords)):
        if x  + 1< len(targetWords):
            iterations = iterations + 1
            try:
                inner_probability = frequency_bigrams[targetWords[x], targetWords[x+1]] / frequency_unigrams[targetWords[x]]
                probability = probability * inner_probability
                print(targetWords[x], " ", targetWords[x+1], " ", frequency_bigrams[targetWords[x], targetWords[x + 1]], " ", frequency_unigrams[targetWords[x]], " ",  inner_probability)
            except:  #unseen bibram
                probability = probability * frequency_unigrams[targetWords[x]] / number_of_words
                print(targetWords[x], " ", targetWords[x+1], "0 ", frequency_unigrams[targetWords[x+1]], " 0.0 *backoff: ", frequency_unigrams[targetWords[x+1]] / number_of_words)
    print("=====================================================")
    print("Bigram probability for sentence ", probability)
    entropy = calculate_entropy(probability, len(tokenize(targetSentence)))
    print("Geometric mean ",  probability**(1/float(iterations)))
    print("Entropy rate: ", entropy)
    perplexity = math.pow(2, entropy)
    print("Perplexity: ", perplexity)
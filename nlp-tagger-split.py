#!/usr/bin/env python3

"""
  nlp-tagger-split.py
  Categorizing and Tagging Words
  Exercise 5-42

  Purpose: Investigate three different ways to define the split between training and testing data
  when developing a tagger using the Brown Corpus: genre (category), source (fileid), and sentence.

  Functionality:
  - The program uses a bigram tagger with the Brown Corpus as the dataset.
  - The tagger is evaluated using three different methods of splitting the test/train datasets
    (by category, by fileid, and all sentences).
  - The program evaluates performance when the train/test datasets are created from
    the same or different corpus sections (category, fileid).
  - The program also evaluates performance using 10-fold cross-validation.

  Challenges: There are a number of ways to evaluate performance, but I chose to keep it simple.
    It was a little difficult to implement 10-fold cross-validation since there were no code
    examples in the book to refer to.
"""

import nltk
from nltk.corpus import brown

import random
import numpy as np
from sklearn.model_selection import KFold


def bigram_tagger_shuffle(tagged_sents):
    """
    Bigram tagger that randomly shuffles the given data between train and test
    """
    # Randomly assigning sentences
    random.shuffle(tagged_sents)
    size = int(len(tagged_sents) * 0.1)
    train_set, test_set = tagged_sents[size:], tagged_sents[:size]

    # We split the data, training on 90% and testing on the remaining 10%
    # size = int(len(tagged_sents) * 0.9)
    # train_sents = tagged_sents[:size]
    # test_sents = tagged_sents[size:]

    # Most NLTK taggers permit a backoff-tagger to be specified.
    t0 = nltk.DefaultTagger("NN")
    t1 = nltk.UnigramTagger(train_set, backoff=t0)
    t2 = nltk.BigramTagger(train_set, backoff=t1)

    # Score the accuracy of the tagger against the gold standard.
    accuracy = t2.evaluate(test_set)

    return accuracy


def bigram_tagger(train_set, test_set):
    """
    Bigram tagger that is given distinct train and test sets
    """
    # random.shuffle(tagged_sents)
    # size = int(len(tagged_sents) * 0.1)
    # train_set, test_set = tagged_sents[size:], tagged_sents[:size]

    # Most NLTK taggers permit a backoff-tagger to be specified.
    t0 = nltk.DefaultTagger("NN")
    t1 = nltk.UnigramTagger(train_set, backoff=t0)
    t2 = nltk.BigramTagger(train_set, backoff=t1)

    # Score the accuracy of the tagger against the gold standard.
    accuracy = t2.evaluate(test_set)

    return accuracy


def bigram_tagger_nfold(tagged_sents):
    """
    Bigram tagger using 10-fold cross-validation

    We randomly choose a training and test set division of our data, train the classiﬁer,
    and compute the error rate on the test set. Then we repeat with a different
    randomly selected training set and test set. We do this sampling process 10 times
    and average the 10 runs to get an average error rate.
    """
    kf = KFold(n_splits=10)

    sum = 0
    i = 1
    for train, test in kf.split(tagged_sents):
        y_train = list(np.array(tagged_sents)[train])
        y_test = list(np.array(tagged_sents)[test])
        accuracy = bigram_tagger(y_train, y_test)
        sum += accuracy
        print(f"{i:2}: {accuracy}")
        i += 1
    average = sum / 10

    return average


def perform(categories=None, fileids=None):
    """
    Evaluate performance of bigram tagger
    """
    if categories is not None:
        brown_tagged_sents = brown.tagged_sents(categories=categories)
    elif fileids is not None:
        brown_tagged_sents = brown.tagged_sents(fileids=fileids)
    else:
        brown_tagged_sents = brown.tagged_sents()

    # What is the upper limit to the performance of an n-gram tagger?
    # How many cases of part-of-speech ambiguity does it encounter?
    # Given the current word and the previous tag, and assuming we always pick
    # the most likely tag in such ambiguous contexts, we can derive a lower bound
    # on the performance of a bigram tagger.
    cfd = nltk.ConditionalFreqDist(
        ((x[1], y[0]), y[1]) for sent in brown_tagged_sents for x, y in nltk.bigrams(sent)
    )
    ambiguous_contexts = [c for c in cfd.conditions() if len(cfd[c]) > 1]
    ambiguous_avg = sum(cfd[c].N() for c in ambiguous_contexts) / cfd.N()

    print(f"ambiguous_avg: {ambiguous_avg}")


def main():

    #
    # train/test using same dataset
    #
    print("train/test using same dataset:\n")

    tagged_sents = list(brown.tagged_sents(categories="news"))
    accuracy_default_category = bigram_tagger_shuffle(tagged_sents)
    print(f"category: {accuracy_default_category:.16}")

    tagged_sents = list(brown.tagged_sents(fileids=["ca16", "ca17", "ca18"]))
    accuracy_default_file = bigram_tagger_shuffle(tagged_sents)
    print(f"file:     {accuracy_default_file:.16}")

    tagged_sents = list(brown.tagged_sents())
    accuracy_default_sentence = bigram_tagger_shuffle(tagged_sents)
    print(f"sentence: {accuracy_default_sentence:.16}")

    print()

    # Evaluate performance of bigram tagger
    perform(categories="news")
    perform(fileids=["ca16", "ca17", "ca18"])
    perform()

    #
    # train/test using different datasets
    #
    print("\ntrain/test using different datasets:\n")

    train_set = list(brown.tagged_sents(categories="news"))
    test_set = list(brown.tagged_sents(categories="fiction"))
    accuracy_diff_category = bigram_tagger(train_set, test_set)
    print(f"category: {accuracy_diff_category:.16}")
    # compute percentage change
    pct_change = (
        (accuracy_diff_category - accuracy_default_category)
        / accuracy_default_category
        * 100
    )
    print(f"change:   {pct_change:<3.4}%\n")

    train_set = list(brown.tagged_sents(fileids=["ca16", "ca17", "ca18"]))
    test_set = list(brown.tagged_sents(fileids=["cb10", "cb11", "cb12"]))
    accuracy_diff_file = bigram_tagger(train_set, test_set)
    print(f"file:     {accuracy_diff_file:.16}")
    # compute percentage change
    pct_change = (
        (accuracy_diff_file - accuracy_default_file) / accuracy_default_file * 100
    )
    print(f"change:   {pct_change:<3.4}%\n")
    # bigram_tagger: 0.6901408450704225

    tagged_sents = list(brown.tagged_sents())
    # Randomly assigning sentences
    random.shuffle(tagged_sents)
    size = int(len(tagged_sents) * 0.1)
    train_set, test_set = tagged_sents[size:], tagged_sents[:size]
    accuracy_diff_sentence = bigram_tagger(train_set, test_set)
    print(f"sentence: {accuracy_diff_sentence:.16}")
    # compute percentage change
    pct_change = (
        (accuracy_diff_sentence - accuracy_default_sentence)
        / accuracy_default_sentence
        * 100
    )
    print(f"change:   {pct_change:<3.4}%\n")

    #
    # train/test sets using same dataset with 10-fold cross-validation
    #
    print("train/test using same dataset with 10-fold cross-validation:\n")

    tagged_sents = list(brown.tagged_sents(categories="news"))
    average_category = bigram_tagger_nfold(tagged_sents)
    print(f"category: {average_category:.16}")
    # compute percentage change
    pct_change = (
        (average_category - accuracy_default_category) / accuracy_default_category * 100
    )
    print(f"change:   {pct_change:<3.4}%\n")

    tagged_sents = list(brown.tagged_sents(fileids=["ca16", "ca17", "ca18"]))
    average_file = bigram_tagger_nfold(tagged_sents)
    print(f"file:     {average_file:.16}")
    # compute percentage change
    pct_change = (average_file - accuracy_default_file) / accuracy_default_file * 100
    print(f"change:   {pct_change:<3.4}%\n")

    tagged_sents = list(brown.tagged_sents())
    average_sentence = bigram_tagger_nfold(tagged_sents)
    print(f"sentence: {average_sentence:.16}")
    # compute percentage change
    pct_change = (
        (average_sentence - accuracy_default_sentence) / accuracy_default_sentence * 100
    )
    print(f"change:   {pct_change:<3.4}%")


if __name__ == "__main__":
    print()
    main()

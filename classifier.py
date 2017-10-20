#!/usr/bin/python

import pdb
from collections import Counter

class Classifier(object):

    def __init__(self, data):
        self.data = data

    def pre_process(self):
        # TODO put text to lower case
        raise NotImplemented

    def train(self):
        raise NotImplemented

    def classify(self, query):
        raise NotImplemented

    def evaluate(self):
        pass

class BayesianClassifier(Classifier):
    pass

    #def __init__(self, data):
        #data.category_counter = Counter()
        #for category in data.categories:
        #    category.update({'char_counter' : Counter()})

class NaiveBayesianClassifier(BayesianClassifier):

    def __init__(self, data):
        super(NaiveBayesianClassifier, self).__init__(data)

    def train(self):

        self.char_counters= {}
        self.category_counter = Counter()
        for utterance in self.data.values():
            # Tally category occurrences
            self.category_counter.update((utterance.category,))
            # Tally only the unique occurrence of each character in the utt
            self.char_counters.setdefault(
                    utterance.category, Counter()).update(Counter(utterance.text).keys())

        self.character_probabilities = {category : {
            char : (
                float(self.char_counters[category][char]) /
                float(self.category_counter[category]))
            for char in self.char_counters[category]}
            for category in self.category_counter.keys()}


    def classify(self, utt):
        utterance_observation = Counter(utt.text)

        maximum = 0
        best_category = None
        for category in self.category_counter.keys():
            category_probability = (float(len(self.category_counter.keys())) /
                    float(self.category_counter[category]))

            likelihood =  reduce(lambda x, y: x * y,
                    [self.character_probabilities[category].get(char, 0)
                        for char in utterance_observation.keys()]
                    + [category_probability])

            if likelihood > maximum:
                maximum = likelihood
                best_category = category

        return best_category

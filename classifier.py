#!/usr/bin/python

import pdb
from collections import Counter

class Classifier(object):
    """Interface for classifier objects"""

    def __init__(self, unprocessed_data):
        """Process and train the classifier given some data"""
        self.data = self.__pre_process__(unprocessed_data)
        self.__train__()

    def __pre_process__(self, data):
        """non-destructively pre-process the data"""
        # Put all text to lower case
        return {key : tpl._replace(text=tpl.text.lower())
                for key, tpl in data.items()}

    def __pre_process_query(self, query):
        # Put all text to lower case
        return query._replace(text=query.text.lower())

    def __train__(self):
        """Train the model"""
        pass

    def classify(self, query):
        """Classify something!"""
        pass

    def evaluate(self, testing_data):
        """Run evaluation metrics on a test set"""
        evaluation = Counter(self.classify(utterance) == utterance.category
                for utterance in testing_data.values())
        return float(evaluation[True]) / float(evaluation[True] + evaluation[False])

class BayesianClassifier(Classifier):
    pass

class NaiveBayesianClassifier(BayesianClassifier):

    def __train__(self):
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
        # pre process query (e.g., conver to lower case)
        utterance_observation = Counter(__pre_process_query__(utt).text)

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

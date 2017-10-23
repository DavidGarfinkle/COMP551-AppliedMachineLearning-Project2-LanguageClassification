#!/usr/bin/python

import pdb
from collections import Counter

class Classifier(object):
    """Interface for classifier objects"""

    def __init__(self, unprocessed_data):
        """Process and train the classifier given some data"""
        self.data = self.__pre_process__(unprocessed_data)

    def __pre_process_utterance__(self, utt):
        # Put to lower case
        processed_utt = utt._replace(text=utt.text.lower())
        # Remove spaces
        processed_utt = processed_utt._replace(
                text=''.join(c for c in processed_utt.text if c != ' '))

        return processed_utt


    def __pre_process__(self, data):
        """non-destructively pre-process the data"""
        # Put all text to lower case
        return [self.__pre_process_utterance__(utt) for utt in data]

        # TODO remove spaces?

    def __pre_process_query__(self, query):
        # Put all text to lower case
        return query._replace(text=query.text.lower())

    def train(self):
        """Train the model"""
        pass

    def classify(self, query):
        """Classify something!"""
        pass


    def evaluate(self, testing_data):
        """Run evaluation metrics on a test set"""
        accuracy = Counter(self.classify(utterance) == utterance.category
                for utterance in testing_data)
        return float(accuracy[True]) / sum(accuracy.values())

class BayesianClassifier(Classifier):
    pass

class NaiveBayesianClassifier(BayesianClassifier):

    def __pre_process__(self, data):
        processed_data = super(NaiveBayesianClassifier, self).__pre_process__(data)

        category_occurrences = Counter(utterance.category for utterance in processed_data)

        # Weird, python won't let me assign an additional attribute to a dictionary subclass 
        self.data_category_frequencies = {category :
                (float(category_occurrences[category]) / float(sum(category_occurrences.values())))
            for category in category_occurrences.keys()}

        return processed_data

    def character_probabilities_by_unique_occurrence(self):
        """
        Calculates the conditional probabilities of characters given a category
        by counting the unique occurrences of a character given an utterance
        from the training set.

        >>> data = [Utterance(0, 'foo'), Utterance(1, 'bar')]
        >>> character_probabilities_by_frequency(data)
        >>> {0 : {'o' : 1, 'f' : 1}, 1 : {'b' : 1, 'a' : 1, 'r': 1}}
        """
        character_count = {}
        for utterance in self.data:
            character_count.setdefault(utterance.category, Counter()).update(
                    Counter(utterance.text).keys())

        return {category :
                {char : float((character_count[category][char]) /
                    float(self.data_category_frequencies[category]))
                    for char in character_count[category]}
                for category in self.data_category_frequencies}

    def character_probabilities_by_frequency(self):
        """
        Calculates the conditional character probabilities given a category.

        Takes the frequency of a character over all characters within a category
        of the training set.

        >>> data = [Utterance(0, 'fool'), Utterance(1, 'bard')]
        >>> character_probabilities_by_frequency(data)
        >>> {0 : {'o' : 0.50, 'f' : 0.25, 'l' : 0.25},
                1 : {'b' : 0.25, 'a' : 0.25, 'r': 0.25, 'd' : 0.25}}
        """
        # Total count of characters among all utterances in the dataset
        character_count = {}
        for utterance in self.data:
            character_count.setdefault(utterance.category, Counter()).update(
                    Counter(utterance.text))

        return {category :
                {char : float((character_count[category][char]) /
                    float(sum(character_count[category].values())))
                    for char in character_count[category]}
                for category in self.data_category_frequencies}

    def train(self, *args):
        self.conditional_char_probabilities = (self.character_probabilities_by_frequency() if 'frequency' in args
                else self.character_probabilities_by_unique_occurrence())

    def __train__old(self):
        self.char_counters= {}
        self.category_counter = Counter()
        for utterance in self.data:
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
        utterance_observation = Counter(self.__pre_process_utterance__(utt).text)

        results = []
        for category in self.data_category_frequencies:
            conditional_probabilities = [
                    self.conditional_char_probabilities[category].get(char, 0)
                    for char in utterance_observation]

            # TODO USE LOG LIKELIHOOD!! will have more accurate numbers
            likelihood = reduce(lambda x, y: x * y,
                    conditional_probabilities + [self.data_category_frequencies[category]])

            results.append((likelihood, category))

        probability, category = max(results)
        return category

    def classify_old(self, utt):
        # pre process query (e.g., conver to lower case)
        utterance_observation = Counter(self.__pre_process_utterance__(utt).text)

        maximum = 0
        best_category = None
        for category in self.category_counter.keys():
            category_probability = (float(len(self.category_counter.keys())) /
                    float(self.category_counter[category]))

            likelihood =  reduce(lambda x, y: x * y,
                    [self.character_probabilities[category].get(char, 0)
                        for char in utterance_observation]
                    + [category_probability])

            if likelihood > maximum:
                maximum = likelihood
                best_category = category

        return best_category


class KNN(Classifier):

    def __init__(self, data, K):
        super(KNN, self).__init__(data)
        self.K = K

    def CNN_data_reduction(self):
        pass
        # 1) Remove outliers



    def utterance_euclidean_distance(self, utt1, utt2):
        import math
        utt1_chars = Counter(utt1.text)
        utt2_chars = Counter(utt2.text)

        return math.sqrt(
                sum(math.pow(utt2_chars[char] - utt1_chars[char], 2)
                    for char in set(utt1_chars.keys() + utt2_chars.keys())))

    def euclidean_distance(self, v1, v2):
        import math

        return math.sqrt(sum(math.pow(v2[i] - v1[i], 2) for i in range(len(v1))))

    def get_utterance_vector(self, utt):
        v = [0 for n in self.characters]
        character_count = Counter(utt.text)

        for c in character_count:
            v[self.character_dimension[c]] = character_count[c]
        return (utt, v)

    def train(self):
        pass
        #self.utterance_vectors = [self.get_utterance_vector(utt) for utt in self.data]

    def classify(self, utt):
        # Get distances to all training points
        distances = sorted([(
            self.utterance_euclidean_distance(utt, neighbor_utt),
            neighbor_utt)
                for neighbor_utt in self.data])

        # count categories of K nearest neighbors
        category_vote = Counter(neighbor_utt.category
                for distance, neighbor_utt in distances[:self.K])
        winner = category_vote.most_common(1)[0]

        # lazy learn
        classified_utt = utt._replace(category = winner)
        self.data.append(utt)

        # return the most common category (the first part of the first tpl of a list)
        return category_vote.most_common(1)[0][0]


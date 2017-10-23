#!/usr/bin/python

import data_parser
import classifier

TRAIN_SET_TEXT_PATH = 'data/train_set_x.csv'
TRAIN_SET_LABELS_PATH = 'data/train_set_y.csv'
TEST_SET_TEXT_PATH = 'data/test_set_x.csv'

def classify_unlabeled_data(classifier, data):
    """Replace the categories of all unlabeled data with model-predicted ones"""
    for i in range(len(data)):
        data[i] = data[i]._replace(category = classifier.classify(data[i]))

def cross_validate(n):
    pass


def run():
    data = data_parser.DataModel(TRAIN_SET_TEXT_PATH, TRAIN_SET_LABELS_PATH)

    training_data_divisor = int(0.8 * len(data))
    training_data = data[training_data_divisor:]
    testing_data = data[:training_data_divisor]

    my_classifier = classifier.KNN(training_data, 2)
    my_classifier.evaluate(testing_data)

    #my_classifier = classifier.NaiveBayesianClassifier(training_data)

    #my_classifier.train('frequency')
    #print('frequency' + str(my_classifier.evaluate(testing_data)))

    #my_classifier.train('occurrence')
    #print('occ' + str(my_classifier.evaluate(training_data)))


training_data = data_parser.DataModel(TRAIN_SET_TEXT_PATH, TRAIN_SET_LABELS_PATH)
#my_classifier = classifier.NaiveBayesianClassifier(training_data)
#my_classifier.train('frequency')

#test_data = data_parser.DataModel(TEST_SET_TEXT_PATH)
#classify_unlabeled_data(my_classifier, test_data)

#test_data.write('test.csv')

my_classifier = classifier.KNN(training_data, 2)
my_classifier.train()
my_classifier.classify(training_data[0])



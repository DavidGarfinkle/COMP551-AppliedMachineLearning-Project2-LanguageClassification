#!/usr/bin/python

import data_parser
import classifier

TRAIN_SET_TEXT_PATH = 'data/train_set_x.csv'
TRAIN_SET_LABELS_PATH = 'data/train_set_y.csv'
TEST_SET_TEXT_PATH = 'data/test_set_x.csv'

training_data = data_parser.DataModel(TRAIN_SET_TEXT_PATH, TRAIN_SET_LABELS_PATH)
#testing_data = data_parser.DataModel(TEST_SET_TEXT_PATH)

my_classifier = classifier.NaiveBayesianClassifier(training_data)






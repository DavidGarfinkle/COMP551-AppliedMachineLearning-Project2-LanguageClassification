#!/usr/bin/python

import data_parser
import classifier

TRAIN_SET_TEXT_PATH = 'data/train_set_x.csv'
TRAIN_SET_LABELS_PATH = 'data/train_set_y.csv'

data = data_parser.DataModel(TRAIN_SET_TEXT_PATH, TRAIN_SET_LABELS_PATH)

my_classifier = classifier.NaiveBayesianClassifier(data)
my_classifier.train()



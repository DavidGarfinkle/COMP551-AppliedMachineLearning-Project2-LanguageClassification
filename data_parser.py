import csv
from collections import namedtuple

class DataModel(dict):
    """Stores data in-memory as a dict of namedtuples"""

    Utterance = namedtuple('Utterance', ['text', 'category'])

    Categories = [
        'slovak',
        'french',
        'spanish',
        'german',
        'polish']

    def __init__(self, text_path, labels_path = None):
        # Parse the csv file with Id : Text data
	with open(text_path, 'r') as f:
            text_dict = dict((int(elt['Id']), elt['Text']) for elt in csv.DictReader(f))

        # Parse the csv file with Id : Category data
        if labels_path:
            with open(labels_path, 'r') as f:
                labels_dict = dict((int(elt['Id']), int(elt['Category'])) for elt in csv.DictReader(f))
        else:
            labels_dict = {key : None for key in text_dict}

        # Build a dictionary of namedtuples combining both dictionaries
	# (Assume dictionaries are of equal length and identical keys)
	super(DataModel, self).__init__(
            (id, DataModel.Utterance(text=text_dict[id], category=labels_dict[id]))
            for id in text_dict.keys())

    def write(self):
        """ Writes two separate Id : Text and Id : Category csv files"""
        pass


class Category(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.char_counter = Counter()

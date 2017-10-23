import csv
from collections import namedtuple

class DataModel(list):
    """Stores data in-memory as a dict of namedtuples"""

    Utterance = namedtuple('Utterance', ['identifier', 'text', 'category'])

    Categories = [
        'Slovak',
        'French',
        'Spanish',
        'German',
        'Polish']

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
            (DataModel.Utterance(identifier = ident, text=text_dict[ident], category=labels_dict[ident]))
            for ident in text_dict)

    def compute_category_counters(self):
        return {category : Counter(utterance.category for utterance in self)}

    def compute_character_counters(self):
        character_count = {}
        for utt in self.data:
            character_count.setdefault(utterance.category, Counter()).update(
                    Counter(utterance.text).keys())

    def write(self, output_path = 'output.csv'):
        """ Writes two separate Id : Text and Id : Category csv files"""
        with open(output_path, 'w') as f:
            writer = csv.DictWriter(f, ['Id', 'Category'])
            writer.writeheader()
            writer.writerows({
                'Id' : utt.identifier,
                'Category' : utt.category}
                for utt in self)


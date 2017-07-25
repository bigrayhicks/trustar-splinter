import pickle
import os
from constants import data_dir, data_name, \
                      num_predictions, model_name, features_name

def load_pickled_model(file_dir=data_dir, file_name=model_name):
    """Loads a pickled sklearn machine learning model.

    :param file_dir: the directory the pickled file is located in.
    :param file_name: The name of the pickled file.
    :return a classifier that was built using the sklearn library.
    """
    abspath = os.path.join(os.path.dirname(__file__),
                           os.path.pardir,
                           file_dir,
                           file_name)
    with open(abspath, 'rb') as f:
        return pickle.load(f)

def load_features_file(file_dir=data_dir, file_name=features_name):
    """Loads a text file of features

    :param file_dir: the directory the text file is located in.
    :param file_name: the name of the text file.
    :return: each line in the text file is returned as an entry in a list.
    """
    abspath = os.path.join(os.path.dirname(__file__),
                           os.path.pardir,
                           file_dir,
                           file_name)
    with open(abspath, 'rb') as f:
        result = [line.replace('\n', '') for line in f]
    return result

def display_prediction(prediction, label):
    """Generates a sentence for the prediction and rat label pair.

    :param prediction: Float from 0 to 100 representing probability.
    :param label: Name of RAT.
    :returns: String output providing a description of what the prediction is.
    """
    return "The IOCs are predicted to be associated with {}".format(label) + \
     " with a probability of {:2.2f}%".format(prediction)

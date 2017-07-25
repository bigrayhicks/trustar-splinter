"""A script used to predict whether a RAT is associated  """
import numpy as np
import pandas as pd
import sys
import os
from utils import load_pickled_model, load_features_file, display_prediction
from constants import data_dir, data_name, num_predictions

BARNCAT_CSV = os.path.join(os.path.dirname(__file__),
                           os.path.pardir,
                           data_dir,
                           data_name)

def parse_clargs(args):
    """Determines if a file or the indicators were sent in as arguments in the
    command line.

    :param args: The command line arguments.
    :returns: A list of IOCs or None if there is an issues.
    """
    if len(args) == 1:
        print("Please include either a file of IOCs or space separated IOCs.")
        print("         python splinter.py <file> <IOCs...>")
        return None
    if os.path.isabs(args[1]) and os.path.isfile(args[1]):
        return extract_iocs(args[1])
    elif os.path.isfile(args[1]):
        return extract_iocs(args[1])
    else:
        return args[1:]

def extract_iocs(filepath):
    """Uses a file and extracts IOCs delimited by a newline or a comma.

    :param filepath: The location of the file.
    :returns: A list of IOCs.
    """
    with open(filepath, 'rb') as f:
        file_text = f.read()
    iocs = file_text.encode('ascii', 'ignore').replace(' ', '')
    iocs = iocs.replace('\r', '').replace(',', '\n').split("\n")
    while '' in iocs:
        iocs.remove('')
    return iocs

def compute_feature_matrix(features, indicators):
    """Generates a feature matrix to be used with the splinter model.

    :parama features: The label names for the features
    :param indicators: The indicators which are used to make a prediction
    :returns: A feature matrix if succesful, None otherwise.
    """
    try:
        data = pd.read_csv(BARNCAT_CSV, index_col=0)
    except Exception as error:
        return None
    value_counts = data.query('indicator in @indicators')['label'].value_counts()
    if len(value_counts) == 0:
        return None
    df = pd.DataFrame()
    for feat in features:
        if feat in value_counts:
            df[feat] = [value_counts[feat]]
        else:
            df[feat] = [0]
    return df[features].values


def generate_prediction_output(predictions, labels, n=5):
    """Produces an output string used to display the n most probable rats.

    :param predictions: A list of probabilities from a model.
    :param labels: A list of rat labels which correspond one-to-one with the
    predictions list.
    :param n: The number of predictions to be displayed in descending order.
    :returns: A string of message for each RAT.
    """
    sort_indices = sorted(range(len(predictions)), key=lambda k: predictions[k])
    message = ""
    prediction_pairs = [(predictions[i] * 100, labels[i]) for i in sort_indices[::-1]]
    for idx in range(n):
        message += display_prediction(prediction_pairs[idx][0],
                                      prediction_pairs[idx][1]) + "\n"
    return message

def main():
    """Uses the command line arguments to generate a list of IOCs. Then a
    classifier is loaded and used to predict the connection to a RAT. These
    predictions are used to generate a message displayed in the command line.
    """
    iocs = parse_clargs(sys.argv)
    if iocs is not None:
        classifier = load_pickled_model()
        feature_labels = load_features_file()
        rat_labels = load_features_file(file_name='rat_labels.txt')
        feature_matrix = compute_feature_matrix(feature_labels, iocs)
        if feature_matrix is not None:
            prediction_probabilities = classifier.predict_proba(feature_matrix)[0]
            print generate_prediction_output(prediction_probabilities,
                                             rat_labels,
                                             n=num_predictions)


if __name__ == '__main__':
    main()

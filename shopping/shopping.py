import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []

    with open(filename) as f:
        contents = f.read().splitlines()[1:]
        for line in contents:
            evidences = []
            columns = line.split(',')
            evidences.append(int(columns[0]))
            evidences.append(float(columns[1]))
            evidences.append(int(columns[2]))
            evidences.append(float(columns[3]))
            evidences.append(int(columns[4]))
            evidences.append(float(columns[5]))
            evidences.append(float(columns[6]))
            evidences.append(float(columns[7]))
            evidences.append(float(columns[8]))
            evidences.append(float(columns[9]))
            evidences.append(parse_month(columns[10]))
            evidences.append(int(columns[11]))
            evidences.append(int(columns[12]))
            evidences.append(int(columns[13]))
            evidences.append(int(columns[14]))
            evidences.append(parse_visitor_type(columns[15]))
            evidences.append(parse_bool(columns[16]))
            
            # append to final lists
            evidence.append(evidences)
            labels.append(parse_bool(columns[17]))
    
    return evidence, labels


def parse_month(month_str):
    """
    Converts from string Month to 0-11
    """
    if month_str == "Jan": 
        return 0
    elif month_str == "Feb": 
        return 1
    elif month_str == "Mar":
        return 2
    elif month_str == "Apr": 
        return 3
    elif month_str == "May": 
        return 4
    elif month_str == "June": 
        return 5
    elif month_str == "Jul": 
        return 6
    elif month_str == "Aug": 
        return 7
    elif month_str == "Sep": 
        return 8
    elif month_str == "Oct": 
        return 9
    elif month_str == "Nov": 
        return 10
    elif month_str == "Dec": 
        return 11
    else: 
        raise ValueError("Invalid month " + month_str)
    

def parse_visitor_type(visitor_type_str):
    """
    Converts from Returning_Visitor or New_Visitor into 1 or 0
    """
    return 1 if visitor_type_str == "Returning_Visitor" else 0


def parse_bool(bool_str):
    """
    Converts from TRUE or FALSE into 1 or 0 
    """
    return 1 if bool_str == "TRUE" else 0


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    return model.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    bought = 0
    bought_and_identified = 0
    not_bought = 0
    not_bought_and_identified = 0

    for label, prediction in zip(labels, predictions):
        if label == 1:
            bought += 1
            if prediction == 1:
                bought_and_identified += 1
        else:
            not_bought += 1
            if prediction == 0:
                not_bought_and_identified += 1

    return bought_and_identified/bought, not_bought_and_identified/not_bought
    

if __name__ == "__main__":
    main()

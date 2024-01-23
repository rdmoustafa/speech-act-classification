import pandas as pd

# TODO sentence preprocessing, turn big paragraphs into single sentences

file_path = "../interrater_data.xlsx"
# Read the Excel file into a pandas DataFrame
excel_file = pd.read_excel(file_path)


# This returns the corresponding labels and sentences separately
def get_sentences_labels():
    labels = []
    for col in excel_file.columns[3:]:
        labels.append(col)

    sentences = []
    correct_labels = []

    for row in excel_file.iterrows():
        for index, speech_act in enumerate(row[1].iloc[3:]):
            if speech_act == "x":
                sentences.append(row[1].iloc[2].lower())
                correct_labels.append(labels[index])
                break

    print("Sentences: ", sentences[:5])
    print("I have sentences: ", len(sentences))
    print("Correct Labels: ", correct_labels[:5])
    print("I have labels: ", len(correct_labels))

    return sentences, correct_labels


# This version returns a list of tuples - Currently not used
def get_labelled_data():
    labels = []
    for col in excel_file.columns[3:]:
        labels.append(col)

    # Extract labels from columns D1 to L1
    # Assuming that 'x' indicates the presence of the corresponding speech act
    # This also assumes that the header location is the same, fixme to do it based on header names
    labelled_data = []
    for row in excel_file.iterrows():
        for index, speech_act in enumerate(row[1].iloc[3:]):
            if speech_act == "x":
                labelled_data.append((row[1].iloc[2], labels[index]))
                break

    # Display the first few rows of the DataFrame for verification
    print(excel_file.head())

    print(labelled_data)

    return labelled_data

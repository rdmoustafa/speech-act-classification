import pandas as pd

# Read the Excel file into a pandas DataFrame
file_path = "data/interrater_data.xlsx"
excel_file = pd.read_excel(file_path)


# This returns the corresponding labels and sentences separately
def get_sentences_labels():
    # Get the labels being used in this Excel file
    labels = []
    for col in excel_file.columns[3:]:
        labels.append(col)

    sentences = []
    associated_labels = []

    for row in excel_file.iterrows():
        for index, speech_act in enumerate(row[1].iloc[3:]):
            if speech_act == "x":
                sentences.append(row[1].iloc[2].lower())
                associated_labels.append(labels[index])
                break

    print("Sentences: ", sentences[:5])
    print("I have sentences: ", len(sentences))
    print("Correct Labels: ", associated_labels)
    print("I have labels: ", len(associated_labels))

    return sentences, associated_labels

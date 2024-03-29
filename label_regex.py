import pandas as pd
import re  # regular expressions

# Define your regular expressions and corresponding labels
original_patterns = {
    'Communications': r'alpha|bravo|charlie|allcallsigns|roger|over|\^cop\$',
    'Intel (from newspapers)': r'squirrel|steel|conference|soccer|music|football|\^relig\$|\^advert\$|stolen'
                               r'|arrest|festival|family|cottage|interfaith|honda|theft|royal|newspaper|community'
                               r'|princess|visit|\^canad',
    'Situation Awareness': r'\^north\$|\^south\$|\^east\$|\^west\$|\^locat\$|hospital|\^camp\$|police|building'
                           r'|wind|draysend|charville|firwood|greenhill|wychewood|woodside|sunwood|westhill|the '
                           r'copse|esterly|newforest|oldtown|lowtown|newton|black '
                           r'hill|dripshill|malton|hollywood|winterfold|shrawleywood|beaconhill|trenchwood'
                           r'|casltehill|linkwood|underwood|wyreforest|castleton|wildwood|hanley|swanton'
                           r'|holbeechwood|astley|thetfordwood|holvern|langdalewood|thetford|brightwood|epping'
                           r'|worthycopse|breydon|denston|worthington',
    'Fire words': r'\^fire\$|water|replen|\^fill\$|\^burn\$|\^extinguish\$|bowser',
    'Rescue words': r'\^load\$|pax|\^evac\$|\^person\$|\^rescue\$|people',
    'Action words': r'recce|check|\^mov\$|\^send\$|support|try|find|support|\^go\$',
    'Reasoning words': r'suggest|\^belie\$|looks|ignore|think|argue'
}

patterns = {
    "Communications": r"alpha|bravo|charlie|allcallsigns|roger|over|\^cop\$|copy",
    "Intel (from newspapers)": r"squirrel|steel|conference|soccer|music|football|\^relig\$|\^advert\$|stolen"
                               r"|arrest|festival|family|cottage|interfaith|honda|theft|royal|newspaper|community"
                               r"|princess|visit|\^canad",
    "Directions": r'\^north|\^south|\^east|\^west|\blocat\w*\b',
    "Woods": r"firwood|wychewood|woodside|shrawleywood|holbeechwood|hollywood|sunwood|trenchwood|wildwood|brightwood"
             r"|linkwood|underwood|langdalewood|thetfordwood",
    "Buildings": r"hospital|\^camp\$|police|building|wind",
    "Hills and Forests": r"beaconhill|casltehill|greenhill|westhill|black hill|dripshill|newforest|wyreforest",
    "Named Locations": "draysend|charville|the copse|esterly|oldtown|lowtown|newtonmalton|winterfold|castleton|hanley"
                       "|swanton|astley|holvern|thetford|epping|worthycopse|breydon|denston|worthington",
    "Fire words": r"fire|water|replen|\^fill\$|\^burn\$|\^extinguish\$|bowser",
    "Rescue words": r"\^load\$|pax|\^evac\$|\^person\$|\^rescue\$|people",
    "Action words": r"recce|check|\^mov\$|\^send\$|support|try|find|support|\^go\$",
    "Reasoning words": r"suggest|\^belie\$|looks|ignore|think|argue"
}

ordered_patterns = {
        "Rescue words": r"\^load\$|pax|\^evac\$|\^person\$|\^rescue\$|people",
        "Action words": r"recce|check|\^mov\$|\^send\$|support|try|find|support|\^go\$",
        "Reasoning words": r"suggest|\^belie\$|looks|ignore|think|argue",
        "Directions": r'\^north|\^south|\^east|\^west|\blocat\w*\b',
        "Fire words": r"fire|water|replen|\^fill\$|\^burn\$|\^extinguish\$|bowser",
        "Woods": r"firwood|wychewood|woodside|shrawleywood|holbeechwood|hollywood|sunwood|trenchwood|wildwood"
                 r"|brightwood|linkwood|underwood|langdalewood|thetfordwood",
        "Buildings": r"hospital|\^camp\$|police|building|wind",
        "Hills and Forests": r"beaconhill|casltehill|greenhill|westhill|black hill|dripshill|newforest|wyreforest",
        "Intel (from newspapers)": r"squirrel|steel|conference|soccer|music|football|\^relig\$|\^advert\$|stolen"
                                   r"|arrest|festival|family|cottage|interfaith|honda|theft|royal|newspaper|community"
                                   r"|princess|visit|\^canad",
        "Named Locations": "draysend|charville|the copse|esterly|oldtown|lowtown|newtonmalton|winterfold|castleton"
                           "|hanley|swanton|astley|holvern|thetford|epping|worthycopse|breydon|denston|worthington",
        "Communications": r"alpha|bravo|charlie|allcallsigns|roger|over|\^cop\$|copy",
    }

ordered_patterns_freq = {
    "Intel (from newspapers)": r"squirrel|steel|conference|soccer|music|football|\^relig\$|\^advert\$|stolen"
                               r"|arrest|festival|family|cottage|interfaith|honda|theft|royal|newspaper|community"
                               r"|princess|visit|\^canad",
    "Directions": r'\^north|\^south|\^east|\^west|\blocat\w*\b',
    "Hills and Forests": r"beaconhill|casltehill|greenhill|westhill|black hill|dripshill|newforest|wyreforest",
    "Reasoning words": r"suggest|\^belie\$|looks|ignore|think|argue",
    "Action words": r"recce|check|\^mov\$|\^send\$|support|try|find|support|\^go\$",
    "Woods": r"firwood|wychewood|woodside|shrawleywood|holbeechwood|hollywood|sunwood|trenchwood|wildwood"
             r"|brightwood|linkwood|underwood|langdalewood|thetfordwood",
    "Rescue words": r"\^load\$|pax|\^evac\$|\^person\$|\^rescue\$|people",
    "Buildings": r"hospital|\^camp\$|police|building|wind",
    "Fire words": r"fire|water|replen|\^fill\$|\^burn\$|\^extinguish\$|bowser",
    "Named Locations": "draysend|charville|the copse|esterly|oldtown|lowtown|newtonmalton|winterfold|castleton"
                       "|hanley|swanton|astley|holvern|thetford|epping|worthycopse|breydon|denston|worthington",
    "Communications": r"alpha|bravo|charlie|allcallsigns|roger|over|\^cop\$|copy"
}

# Define a regular expression pattern to split the paragraph into sentences
sentence_pattern = r'(?<=[.!?])\s+'


def single_label(path, output):
    # Load the CSV file into a pandas DataFrame
    raw_df = pd.read_csv(path)

    # Split the paragraph into sentences and clean up the unnecessary dots and make it lower case
    raw_sentences = []
    for row in raw_df["Text"]:
        raw_sentences += (re.split(sentence_pattern.lower(), row.lower()))

    clean_sentences = []

    for index, sentence in enumerate(raw_sentences):
        if sentence.strip() == "." or sentence.strip() == "":
            continue
        clean_sentences.append(sentence.replace(".", "").strip())

    # For each sentence, go through the regex and add label them for each one they match to
    labeled_sentences = []

    for sentence in clean_sentences:
        # The goal here is to avoid adding communication for every sentence and just add it for those that are purely
        # communication
        matched_labels = []
        for label_name, pattern in patterns.items():
            if re.search(pattern, sentence):
                matched_labels.append(label_name)
        if len(matched_labels) == 0:
            labeled_sentences.append((sentence, "Other"))
        elif len(matched_labels) == 1:
            labeled_sentences.append((sentence, matched_labels[0]))
        else:
            for match in matched_labels:
                if match != "Communications":
                    labeled_sentences.append((sentence, match))

    # This will make the data set unique, will not repeat the same tuple
    labeled_df = pd.DataFrame(list(set(labeled_sentences)), columns=['Sentence', 'Label'])
    # labeled_df = pd.DataFrame(labeled_sentences, columns=['Sentence', 'Labels'])
    # Save the DataFrame to a CSV file
    labeled_df.to_csv(output, index=False)

    print("Data has been written to: ", output)
    # return labeled_sentences

def single_label_priority(path, output, pattern_to_use):
    # Load the CSV file into a pandas DataFrame
    raw_df = pd.read_csv(path)

    # Split the paragraph into sentences and clean up the unnecessary dots and make it lower case
    raw_sentences = []
    for row in raw_df["Text"]:
        raw_sentences += (re.split(sentence_pattern.lower(), row.lower()))

    clean_sentences = []

    for index, sentence in enumerate(raw_sentences):
        if sentence.strip() == "." or sentence.strip() == "":
            continue
        clean_sentences.append(sentence.replace(".", "").strip())

    # For each sentence, go through the regex and add label them for each one they match to
    labeled_sentences = []

    for sentence in clean_sentences:
        matched_labels = []
        for label_name, pattern in pattern_to_use.items():
            # Priority system for the patterns?
            if re.search(pattern, sentence):
                matched_labels.append(label_name)
                break

        if len(matched_labels) == 0:
            labeled_sentences.append((sentence, "Other"))
        elif len(matched_labels) == 1:
            labeled_sentences.append((sentence, matched_labels[0]))
        else:
            print("Error, should not reach here. Sentence: " + sentence)

    # This will make the data set unique, will not repeat the same tuple
    labeled_df = pd.DataFrame(list(set(labeled_sentences)), columns=["Sentence", "Label"])

    # Save the DataFrame to a CSV file
    labeled_df.to_csv(output, index=False)

    print("Data has been written to: ", output)
    # return labeled_sentences

unique_labels = list(patterns.keys())

def multiclass_labelling(path, output):
    # Load the CSV file into a pandas DataFrame
    raw_df = pd.read_csv(path)

    data_dict = {'Sentence': []}

    for label in unique_labels:
        data_dict[label] = []

    # Split the paragraph into sentences and clean up the unnecessary dots and make it lower case
    raw_sentences = []
    for row in raw_df["Text"]:
        raw_sentences += (re.split(sentence_pattern, row))

    clean_sentences = []

    for index, sentence in enumerate(raw_sentences):
        if sentence.strip() == "." or sentence.strip() == "":
            continue
        clean_sentences.append(sentence.replace(".", "").strip())

    # print(clean_sentences)

    # For each sentence, go through the regex and add label them for each one they match to
    labeled_sentences = []

    for sentence in clean_sentences:
        matched_labels = []
        for label_name, pattern in patterns.items():
            if re.search(pattern, sentence, re.IGNORECASE):
                matched_labels.append(label_name)
        labeled_sentences.append((sentence, matched_labels))

    for sentence, matched_labels in labeled_sentences:
        if "Locations" in matched_labels:
            print(sentence, matched_labels)

        data_dict['Sentence'].append(sentence)
        for label in unique_labels:
            if label in matched_labels:
                data_dict[label].append(1)
            else:
                data_dict[label].append(0)

        # Convert dictionary to DataFrame
    df = pd.DataFrame(data_dict)

    # Save DataFrame to Excel file
    df.to_excel(output, index=False)

    print("Data has been written to ", output)


if __name__ == "__main__":
    # single_label("data/full-raw-transcript.csv", "data/adjusted-labels-comms-exclusive.csv")
    # multiclass_labelling("data/full-raw-transcript.csv", "data/adjusted-labels-multiclass.xlsx")

    single_label_priority("data/full-raw-transcript.csv", "data/adjusted-labels-prioritised-importance.csv", ordered_patterns)
    single_label_priority("data/full-raw-transcript.csv", "data/adjusted-labels-prioritised-frequency.csv", ordered_patterns_freq)

import pandas as pd
import re  # regular expressions


def label_csv(path):
    # Load the CSV file into a pandas DataFrame
    raw_df = pd.read_csv(path)

    # Define your regular expressions and corresponding labels
    patterns = {
        'Communications': r'alpha|bravo|charlie|allcallsigns|roger|over|\^cop\$',
        'Intel (from newspapers)': r'squirrel|steel|conference|soccer|music|football|\^relig\$|\^advert\$|stolen|arrest'
                                   r'|festival|family|cottage|interfaith|honda|theft|royal|newspaper|community|princess'
                                   r'|visit|\^canad',
        'Situation Awareness': r'\^north\$|\^south\$|\^east\$|\^west\$|\^locat\$|hospital|\^camp\$|police|building|wind'
                               r'|draysend|charville|firwood|greenhill|wychewood|woodside|sunwood|westhill|the '
                               r'copse|esterly|newforest|oldtown|lowtown|newton|black '
                               r'hill|dripshill|malton|hollywood|winterfold|shrawleywood|beaconhill|trenchwood|casltehill'
                               r'|linkwood|underwood|wyreforest|castleton|wildwood|hanley|swanton|holbeechwood|astley'
                               r'|thetfordwood|holvern|langdalewood|thetford|brightwood|epping|worthycopse|breydon'
                               r'|denston|worthington',
        'Fire words': r'\^fire\$|water|replen|\^fill\$|\^burn\$|\^extinguish\$|bowser',
        'Rescue words': r'\^load\$|pax|\^evac\$|\^person\$|\^rescue\$|people',
        'Action words': r'recce|check|\^mov\$|\^send\$|support|try|find|support|\^go\$',
        'Reasoning words': r'suggest|\^belie\$|looks|ignore|think|argue'
    }

    # Define a regular expression pattern to split the paragraph into sentences
    sentence_pattern = r'(?<=[.!?])\s+'

    # Split the paragraph into sentences and clean up the unnecessary dots and make it lower case
    raw_sentences = []
    for row in raw_df["Text"]:
        raw_sentences += (re.split(sentence_pattern.lower(), row.lower()))

    clean_sentences = []

    for index, sentence in enumerate(raw_sentences):
        if sentence.strip() == ".":
            continue
        clean_sentences.append(sentence.replace(".", "").strip())

    # For each sentence, go through the regex and add label them for each one they match to
    labeled_sentences = []

    for sentence in clean_sentences:
        for label_name, pattern in patterns.items():
            if re.search(pattern, sentence):
                labeled_sentences.append((sentence, label_name))

    # # Print the labeled sentences
    # for sentence, label in labeled_sentences:
    #     print(f"Sentence: {sentence} | Label: {label}")

    # Convert the data to a pandas DataFrame
    # This will make the data set unique, will not repeat the same tuple
    labeled_df = pd.DataFrame(list(set(labeled_sentences)), columns=['Sentence', 'Labels'])

    # Path to the CSV file
    csv_file = "data/labeled_sentences.csv"

    # Save the DataFrame to a CSV file
    labeled_df.to_csv(csv_file, index=False)

    print("Data has been written to", csv_file)
    return labeled_sentences

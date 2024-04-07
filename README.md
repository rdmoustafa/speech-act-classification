# Speech Act Classification

This project aims to classify speech acts using machine learning techniques. It includes implementations of various models such as Naive Bayes, Support Vector Machine (SVM), Convolutional Neural Network (CNN), and BERT for both single-label and multi-label classification tasks. The code provides functionalities for data preprocessing, model training, evaluation, and comparison.


****

The directory 'data' contains the csv and Excel files for the raw and labelled datasets.
Within data the following files exist:
1. **full-raw-transcript.csv**: the original raw data
2. **original-labels.csv**: contains the sentences labelled following the original labels
3. **adjusted-labels-comms-exclusive.csv**: contains the sentences labelled with the Multiple Instances Labelling approach
4. **adjusted-labels-priorities-importance.csv**: contains the sentence labelled with the Priority Labelling approach
5. **adjusted-labels-multiclass.xlsx**: contains the sentences labelled for multi-label classification

The following directories are named after the machine learning technique implemented in those directories. Each directory contains the code for both single and multi label classification for that machine learning technique
1. bert
2. convolutional-neural-network
3. naive-bayes
4. support-vector-machine

The following files in the root directory are:
1. **data-visualisation.ipynb**: Running this file generates charts and visualisations for the various  data files
2. **label_regex.py**: This file contains several functions that utilise regular expressions to label the original data based on the requirements including priority labelling, multiple instances labelling, and for multi-label classification 

It is important to maintain the structure of the project when running it as the paths are relative to the root directory. 

****

In order to run the code a machine with Python 3.x installed is required. 
Furthermore, in order to run the CNN and BERT models effectively, they need to be run with GPU support such as a platform like Google Colab.

Each jupyter notebook file can be run independently to reproduce the results discussed in the report.  



from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

from model_attempts.preprocessing import get_sentences_labels


sentences, labels = get_sentences_labels()


# Step 3: Preprocessing
# You may need to do more sophisticated preprocessing based on your dataset
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(sentences)

# Step 4: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.20, random_state=42)

# Step 5: Model Selection - this is a basic naive bayes classifier
classifier = MultinomialNB()

# Step 6: Model Training
classifier.fit(X_train, y_train)

# Step 7: Model Evaluation
y_pred = classifier.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Classification Report
print("Classification Report:\n", classification_report(y_test, y_pred, zero_division=0))

# Now you can use the trained model to predict the speech act of new sentences
# 0 = statement, 1 = request, 2 = request
new_sentences = ["i think you're on it rather next to it. you need to be next to it.",
                 "yeah, i'm putting up northwesterly barrier. you see where firetruck_one, firetruck_two and "
                 "firetruck_three are?",
                 "yeah. confirm all fires extinguished?"]
new_X = vectorizer.transform(new_sentences)
new_predictions = classifier.predict(new_X)

# Print predictions for new sentences
for sentence, prediction in zip(new_sentences, new_predictions):
    print(f"Sentence: '{sentence}'\t Predicted Speech Act: {prediction}")

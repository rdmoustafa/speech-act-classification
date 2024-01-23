import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import img_to_array, load_img

# Assuming you have a dataset with X (features) and y (labels)
# X should be a list of paths to image files or a 4D array (number of samples, width, height, channels)
# y should be a 1D array or list with corresponding labels

# Load and preprocess your data
# (Replace this with your actual data loading and preprocessing steps)
X_paths = [...]  # Replace with paths to your image files
y = np.load('your_labels.npy')  # Replace 'your_labels.npy' with your actual file

# Convert labels to one-hot encoding
y_one_hot = tf.keras.utils.to_categorical(y, num_classes=num_classes)

# Load ResNet-50 model pre-trained on ImageNet
resnet_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Extract features using ResNet-50
X_features = []
for path in X_paths:
    img = load_img(path, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.resnet50.preprocess_input(img_array)
    features = resnet_model.predict(img_array)
    X_features.append(features.flatten())

X_features = np.array(X_features)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_features, y_one_hot, test_size=0.2, random_state=42)

# Build a simple classifier on top of ResNet-50 features
model = models.Sequential()
model.add(layers.Dense(256, activation='relu', input_dim=2048))  # 2048 is the size of ResNet-50 features
model.add(layers.Dropout(0.5))
model.add(layers.Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2)

# Evaluate the model on the test set
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f'Test accuracy: {test_acc}')

# Make predictions
predictions = model.predict(X_test)

# You can further analyze the results and fine-tune the model based on your specific requirements

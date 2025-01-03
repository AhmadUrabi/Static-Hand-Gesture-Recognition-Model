from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd

training_df = pd.read_csv("training.csv")
x_train = training_df.iloc[:, :-1]
y_train = training_df.iloc[:, -1]
print("Train set imported")

validation_df = pd.read_csv("validation.csv")
x_val = validation_df.iloc[:, :-1]
y_val = validation_df.iloc[:, -1]
print("Valid set imported")

test_df = pd.read_csv("testing.csv")
x_test = test_df.iloc[:, :-1]
y_test = test_df.iloc[:, -1]
print("Test set imported")

# Uncomment to change the model
rnd_clf = RandomForestClassifier(n_estimators=500, max_leaf_nodes=48, n_jobs=-1)
# rnd_clf = KNeighborsClassifier(n_neighbors=5)
# rnd_clf = SVC(kernel='linear',  random_state=42)
rnd_clf.fit(x_train, y_train)
print("Trained")

val_pred = rnd_clf.predict(x_val)
val_accuracy = accuracy_score(y_val, val_pred)

y_pred = rnd_clf.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy}")
print(f"Validation Accuracy: {val_accuracy}")
from sklearn.metrics import f1_score, precision_score, recall_score, classification_report

# Calculate F1 score, precision, and recall for validation set
val_f1 = f1_score(y_val, val_pred, average='weighted')
val_precision = precision_score(y_val, val_pred, average='weighted')
val_recall = recall_score(y_val, val_pred, average='weighted')

# Calculate F1 score, precision, and recall for test set
test_f1 = f1_score(y_test, y_pred, average='weighted')
test_precision = precision_score(y_test, y_pred, average='weighted')
test_recall = recall_score(y_test, y_pred, average='weighted')

print(f"Validation F1 Score: {val_f1}")
print(f"Validation Precision: {val_precision}")
print(f"Validation Recall: {val_recall}")

print(f"Test F1 Score: {test_f1}")
print(f"Test Precision: {test_precision}")
print(f"Test Recall: {test_recall}")

# Print classification report for validation and test sets
print("Validation Classification Report:")
print(classification_report(y_val, val_pred))

print("Test Classification Report:")
print(classification_report(y_test, y_pred))
# Save the model
joblib.dump(rnd_clf, "hand_model.pkl")

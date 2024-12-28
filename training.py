from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

training_df = pd.read_csv("training.csv")
x_train = training_df.iloc[:, 1:-1]
y_train = training_df.iloc[:, -1]

validation_df = pd.read_csv("validation.csv")
x_val = validation_df.iloc[:, 1:-1]
y_val = validation_df.iloc[:, -1]

test_df = pd.read_csv("testing.csv")
x_test = test_df.iloc[:, 1:-1]
y_test = test_df.iloc[:, -1]

rnd_clf = RandomForestClassifier(n_estimators=100, max_leaf_nodes=48, n_jobs=-1)
rnd_clf.fit(x_train, y_train)

val_pred = rnd_clf.predict(x_val)
val_accuracy = accuracy_score(y_val, val_pred)
print(f"Validation Accuracy: {val_accuracy}")

y_pred = rnd_clf.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy}")

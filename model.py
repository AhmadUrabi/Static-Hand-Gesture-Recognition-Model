import joblib
# from sklearn.metrics import accuracy_score
import pandas as pd
import mediapipe as mp
import cv2

rnd_clf = joblib.load("hand_model.pkl")

# Load the test data
test_df = pd.read_csv("testing.csv")
x_test = test_df.iloc[:, 1:-1]
y_test = test_df.iloc[:, -1]

# 0: "Two"
# 1: "Two with palm"
# 2: "Two with palm down"
# 3: "Arms Sideways Facing different sides"
# 4: "Yes"
# 5: "Yesterday"
# 6: "Head"
# 7: "Inside"
# 8: "Leg"
# 9: "Medicine"
# 10: "No"
# 11: "Sick"
# 12: "Snot"
# 13: "Surgery"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        instance = []
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                instance.extend([landmark.x, landmark.y, landmark.z])
        if instance:
            if len(instance) != 126:
                instance.extend(0 for i in range(126 - len(instance)))
            instance_df = pd.DataFrame([instance])
            new_columns = [f'landmark_{i}_{axis}' for i in range(42) for axis in ['x', 'y', 'z']]
            instance_df.columns = new_columns
            prediction = rnd_clf.predict(instance_df)
            print(f"Prediction: {prediction}")

    # cv2.imshow('MediaPipe Hands', image)
    # if cv2.waitKey(5) & 0xFF == 27:
    #     break

cap.release()

# Make predictions
# y_pred = rnd_clf.predict(x_test)
# accuracy = accuracy_score(y_test, y_pred)
# print(f"Test Accuracy: {accuracy}")

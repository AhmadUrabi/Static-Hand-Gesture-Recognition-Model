# Note: to run in nix-os
# nix-shell
# source ./aiproj/bin/activate

import cv2
import mediapipe as mp
import csv

def read_annotations(file):
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(
        static_image_mode=True,
        model_complexity=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
        max_num_hands=1)
    with open(file, mode='r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the first row
        count = 0
        for row in csvreader:
            process_row(f'./dataset/train/{row[0]}', hands, row[3])
            # process row
        print(f'Processed {count} images, data stored in train.csv')


def write_frame_entry(landmarks, filename, classname):
    with open('training.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        print(f'Reading {filename}\n')
        result_row = [f'{filename}']
        for landmark in landmarks.landmark:
            result_row.append(landmark.x)
            result_row.append(landmark.y)
            result_row.append(landmark.z)
        result_row.append(classname)
        writer.writerow(result_row)


def process_row(filename, hands, classname):
    frame = cv2.imread(filename)

    img = cv2.resize(frame, (640, 480))

    # Flip the image(frame)
    img = cv2.flip(img, 1)

    # Convert BGR image to RGB image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the RGB image
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Write landmarks to CSV
            write_frame_entry(hand_landmarks, filename, classname)

            # # Draw circles for each landmark
            # for landmark in hand_landmarks.landmark:
            #     x = int(landmark.x * 640)
            #     y = int(landmark.y * 480)
            #     cv2.circle(img, (x, y), 5, (0, 255, 0), -1)

        # # Save annotated image
        # cv2.imwrite(f"frames/frame{count}.jpg", img)

def main():
    read_annotations('dataset/train/_annotations.csv')
    pass


if __name__ == "__main__":
    main()

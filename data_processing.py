import mediapipe as mp
import csv
import cv2

def read_annotations(file, setName, fileName):
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(
        static_image_mode=True,
        model_complexity=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
        max_num_hands=2)
    with open(file, mode='r') as csvfile:
        with open(f'${fileName}.csv', mode='a', newline='') as file:
            csvreader = csv.reader(csvfile)
            writer = csv.writer(file)
            next(csvreader)  # Skip the first row
            count = 0
            header = []
            for i in range(42):
                header.append(f'landmark_{i}_x')
                header.append(f'landmark_{i}_y')
                header.append(f'landmark_{i}_z')
            header.append('classname')
            writer.writerow(header)
            for row in csvreader:
                process_row(f'./dataset/{setName}/{row[0]}', hands, row[3], writer)
                count += 1;
                # process row
            print(f'Processed {count} images, data stored in {fileName}.csv')


def process_row(filename, hands, classname,writer):
    frame = cv2.imread(filename)

    img = cv2.resize(frame, (640, 480))

    # Flip the image(frame)
    img = cv2.flip(img, 1)

    # Convert BGR image to RGB image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the RGB image
    results = hands.process(imgRGB)
    # If no hand landmarks are found, it will skip over it
    if results.multi_hand_landmarks:
        result_row = []
        print(f'Reading {filename}\n')
        for landmarks in results.multi_hand_landmarks:
            # Write landmarks to CSV
            for landmark in landmarks.landmark:
                result_row.append(landmark.x)
                result_row.append(landmark.y)
                result_row.append(landmark.z)

        # If only one hand is detected, fill the rest with 0.00
        if len(results.multi_hand_landmarks) == 1:
            for _ in range(21):
                result_row.append(0.00)
                result_row.append(0.00)
                result_row.append(0.00)
        result_row.append(classname)
        writer.writerow(result_row)

def main():
    read_annotations('dataset/train/_annotations.csv', 'train', 'training')
    read_annotations('dataset/valid/_annotations.csv', 'valid', 'validation')
    read_annotations('dataset/test/_annotations.csv', 'test', 'testing')
    pass


if __name__ == "__main__":
    main()

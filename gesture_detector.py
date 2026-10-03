import cv2
import mediapipe as mp


class GestureDetector:

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def detect(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if not results.multi_hand_landmarks:
            return None

        hand = results.multi_hand_landmarks[0]

        self.mp_drawing.draw_landmarks(
            frame,
            hand,
            self.mp_hands.HAND_CONNECTIONS
        )

        return self.identify_gesture(hand)

    def identify_gesture(self, hand):
        landmarks = hand.landmark

        index_up = landmarks[8].y < landmarks[6].y
        middle_up = landmarks[12].y < landmarks[10].y
        ring_up = landmarks[16].y < landmarks[14].y
        pinky_up = landmarks[20].y < landmarks[18].y

        if index_up and middle_up and not ring_up and not pinky_up:
            return "PEACE"

        if not index_up and not middle_up and not ring_up and not pinky_up:
            return "BRO"

        if middle_up and not index_up and not ring_up and not pinky_up:
            return "FUCK_YOU"

        if index_up and middle_up and ring_up and pinky_up:
            return "HELLO"

        return None

    def close(self):
        self.hands.close()
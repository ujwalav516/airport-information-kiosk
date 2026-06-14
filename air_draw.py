import cv2
import mediapipe as mp
import numpy as np
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
clear_counter = 0
prev_x = 0
prev_y = 0
canvas = None

while True:
    success, img = cap.read()
    if canvas is None:
        canvas = np.zeros_like(img)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            h, w, c = img.shape

            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            thumb_tip = hand_landmarks.landmark[4]

            cx = int(index_tip.x * w)
            cy = int(index_tip.y * h)
            middle_y = int(middle_tip.y * h)
            thumb_y = int(thumb_tip.y * h)
            thumb_x = int(thumb_tip.x * w)
            distance = math.sqrt((cx - thumb_x)**2 + (cy - thumb_y)**2)
            print("Distance:", distance)
            

            if middle_y < cy:
                cv2.putText(img, "STOP", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 3)
                
                

            if distance < 15:
               clear_counter += 1

               cv2.putText(img, "HOLD TO CLEAR", (50, 100),
                           cv2.FONT_HERSHEY_SIMPLEX,
                           1, (0, 255, 255), 3)

               if clear_counter > 20:
                  canvas = np.zeros_like(img)

            else:
                clear_counter = 0


            if middle_y > cy:
                if prev_x != 0 and prev_y != 0:
                    cv2.line(canvas, (prev_x, prev_y), (cx, cy), (255, 0, 0), 5)

       

            prev_x = cx
            prev_y = cy

            print("Index Finger:", cx, cy)
    img = cv2.add(img, canvas)
    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
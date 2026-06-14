import cv2
import mediapipe as mp

# Hand Tracking Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

page = "home"
selected_city = ""

cx = 0
cy = 0

while True:

    success, img = cap.read()

    if not success:
        break

    h, w, c = img.shape

    overlay = img.copy()
    overlay[:] = (25, 25, 25)

    screen = cv2.addWeighted(
        overlay,
        0.85,
        img,
        0.15,
        0
    )

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # ---------------- HAND TRACKING ----------------

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                screen,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            index_tip = hand_landmarks.landmark[8]

            cx = int(index_tip.x * w)
            cy = int(index_tip.y * h)

    # ---------------- HOME PAGE ----------------

    if page == "home":

        cv2.rectangle(screen, (0, 0), (640, 70), (15, 15, 15), -1)

        cv2.putText(
            screen,
            "AIRPORT INFORMATION KIOSK",
            (80, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        color = (80, 80, 80)

        if 150 < cx < 500 and 120 < cy < 200:
            color = (0, 180, 255)
            page = "destinations"

        cv2.rectangle(
            screen,
            (150, 120),
            (500, 200),
            color,
            -1
        )

        cv2.putText(
            screen,
            "Flight Search",
            (220, 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

    # ---------------- DESTINATIONS PAGE ----------------

    elif page == "destinations":

        screen[:] = (20, 20, 20)

        # BACK BUTTON

        back_color = (100, 100, 100)

        if 20 < cx < 120 and 20 < cy < 70:
            back_color = (0, 180, 255)
            page = "home"

        cv2.rectangle(
            screen,
            (20, 20),
            (120, 70),
            back_color,
            -1
        )

        cv2.putText(
            screen,
            "BACK",
            (35, 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

        cv2.putText(
            screen,
            "SELECT DESTINATION",
            (120, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )

        # DELHI BUTTON

        delhi_color = (70,70,70)

        if 150 < cx < 500 and 150 < cy < 210:
            delhi_color = (0,180,255)

            selected_city = "Delhi"
            page = "flights"

        cv2.rectangle(
            screen,
            (150,150),
            (500,210),
            delhi_color,
            -1
        )

        cv2.putText(
            screen,
            "Delhi",
            (270,190),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )

        # MUMBAI

        cv2.rectangle(
            screen,
            (150,240),
            (500,300),
            (70,70,70),
            -1
        )

        cv2.putText(
            screen,
            "Mumbai",
            (250,280),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )

        # BANGALORE

        cv2.rectangle(
            screen,
            (150,330),
            (500,390),
            (70,70,70),
            -1
        )

        cv2.putText(
            screen,
            "Bangalore",
            (220,370),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )

    # ---------------- FLIGHTS PAGE ----------------

    elif page == "flights":

        screen[:] = (15,15,15)

        cv2.putText(
            screen,
            "FLIGHTS TO " + selected_city.upper(),
            (80,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )

        cv2.putText(
            screen,
            "AI202   10:30 AM",
            (150,170),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

        cv2.putText(
            screen,
            "6E455   12:15 PM",
            (150,240),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

        cv2.putText(
            screen,
            "UK901   03:45 PM",
            (150,310),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

        # BACK BUTTON

        back_color = (100,100,100)

        if 20 < cx < 120 and 20 < cy < 70:
            back_color = (0,180,255)
            page = "destinations"

        cv2.rectangle(
            screen,
            (20,20),
            (120,70),
            back_color,
            -1
        )

        cv2.putText(
            screen,
            "BACK",
            (35,55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

    # ---------------- CURSOR ----------------

    cv2.circle(screen, (cx, cy), 35, (255,255,0), 1)
    cv2.circle(screen, (cx, cy), 25, (255,255,0), 2)
    cv2.circle(screen, (cx, cy), 12, (255,255,0), cv2.FILLED)

    cv2.imshow("Airport Kiosk", screen)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
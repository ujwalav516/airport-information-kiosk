
# AIRPORT KIOSK V5
# Improvements:
# - Hover timer increased to 1.5 sec
# - Cooldown after page changes
# - Hover state reset on page change
# - Back button on every page
# - Seat selection
# - Boarding pass
# - Hand skeleton + cursor

import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

cv2.namedWindow(
    "Airport Kiosk V5",
    cv2.WINDOW_NORMAL
)

cv2.setWindowProperty(
    "Airport Kiosk V5",
    cv2.WND_PROP_FULLSCREEN,
    cv2.WINDOW_FULLSCREEN
)

page = "home"
selected_city = ""
selected_flight = ""
selected_seat = ""

cx, cy = 0, 0

hover_target = None
hover_start = None

last_page_change = 0
COOLDOWN = 0.5
HOVER_TIME = 1.5

flight_data = {
    "Delhi": [
        ("AI202", "10:30 AM", "On Time"),
        ("6E455", "12:15 PM", "Delayed"),
        ("UK901", "03:45 PM", "Boarding")
    ],
    "Mumbai": [
        ("AI105", "09:00 AM", "On Time"),
        ("6E300", "01:00 PM", "Boarding"),
        ("UK777", "05:30 PM", "Delayed")
    ],
    "Bangalore": [
        ("AI501", "08:45 AM", "On Time"),
        ("6E222", "11:20 AM", "On Time"),
        ("UK888", "06:10 PM", "Boarding")
    ]
}

def change_page(new_page):
    global page, hover_target, hover_start, last_page_change

    page = new_page
    hover_target = None
    hover_start = None
    last_page_change = time.time()

def hover_click(name, hovering):

    global hover_target, hover_start

    if time.time() - last_page_change < COOLDOWN:
        return False, None

    if hovering:

        if hover_target != name:
            hover_target = name
            hover_start = time.time()

        elapsed = time.time() - hover_start
        remain = max(0, round(HOVER_TIME - elapsed, 1))

        if elapsed >= HOVER_TIME:
            hover_target = None
            hover_start = None
            return True, 0

        return False, remain

    if hover_target == name:
        hover_target = None
        hover_start = None

    return False, None


while True:

    ok, img = cap.read()

    if not ok:
        break

    h, w, c = img.shape

    overlay = img.copy()
    overlay[:] = (20, 20, 30)

    screen = cv2.addWeighted(
        overlay,
        0.80,
        img,
        0.20,
        0
    )

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                screen,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(
                    color=(0,255,255),
                    thickness=2,
                    circle_radius=3
                ),
                mp_draw.DrawingSpec(
                    color=(255,255,0),
                    thickness=2
                )
            )

            tip = hand_landmarks.landmark[8]

            cx = int(tip.x * w)
            cy = int(tip.y * h)

    # HOME

    if page == "home":

        cv2.putText(
            screen,
            "AIRPORT INFORMATION KIOSK",
            (50,60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255,255,0),
            2
        )

        hover = 150 < cx < 500 and 120 < cy < 200

        clicked, rem = hover_click("search", hover)

        cv2.rectangle(
            screen,
            (150,120),
            (500,200),
            (0,180,255) if hover else (50,50,120),
            -1
        )

        cv2.putText(
            screen,
            "Flight Search",
            (220,170),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )

        if rem is not None:
            cv2.putText(screen,str(rem),(510,170),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,(255,255,255),2)

        if clicked:
            change_page("destinations")

    # DESTINATIONS

    elif page == "destinations":

        screen[:] = (20,20,30)

        cv2.putText(
            screen,
            "SELECT DESTINATION",
            (120,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )

        back_hover = 20 < cx < 120 and 20 < cy < 70

        cv2.rectangle(
            screen,
            (20,20),
            (120,70),
            (0,180,255) if back_hover else (90,90,90),
            -1
        )

        cv2.putText(screen,"BACK",(35,55),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,(255,255,255),2)

        if back_hover:
            change_page("home")

        cities = [
            ("Delhi",150),
            ("Mumbai",240),
            ("Bangalore",330)
        ]

        for city, y in cities:

            hover = 150 < cx < 500 and y < cy < y+60

            clicked, rem = hover_click(city, hover)

            cv2.rectangle(
                screen,
                (150,y),
                (500,y+60),
                (0,180,255) if hover else (60,60,120),
                -1
            )

            cv2.putText(
                screen,
                city,
                (240,y+40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,255,255),
                2
            )

            if rem is not None:
                cv2.putText(screen,str(rem),(520,y+35),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,(255,255,255),2)

            if clicked:
                selected_city = city
                change_page("flights")

    # FLIGHTS

    elif page == "flights":

        screen[:] = (15,15,25)

        cv2.putText(
            screen,
            f"FLIGHTS TO {selected_city.upper()}",
            (70,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,0),
            2
        )

        back_hover = 20 < cx < 120 and 20 < cy < 70

        cv2.rectangle(screen,(20,20),(120,70),
                      (0,180,255) if back_hover else (90,90,90),-1)

        cv2.putText(screen,"BACK",(35,55),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

        if back_hover:
            change_page("destinations")

        y = 130

        for flight,time_text,status in flight_data[selected_city]:

            hover = 100 < cx < 540 and y < cy < y+60

            clicked, rem = hover_click(flight, hover)

            cv2.rectangle(screen,(100,y),(540,y+60),
                          (0,180,255) if hover else (70,70,70),-1)

            cv2.putText(screen,flight,(120,y+38),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,
                        (255,255,255),2)

            cv2.putText(screen,time_text,(250,y+38),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,
                        (255,255,255),2)

            color = (0,255,0)

            if status == "Delayed":
                color = (0,0,255)
            elif status == "Boarding":
                color = (0,165,255)

            cv2.putText(screen,status,(380,y+38),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,color,2)

            if rem is not None:
                cv2.putText(screen,str(rem),(550,y+38),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,(255,255,255),2)

            if clicked:
                selected_flight = flight
                change_page("details")

            y += 90

    elif page == "details":

        screen[:] = (20,20,30)

        cv2.putText(screen,"FLIGHT DETAILS",
                    (170,80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,255,0),2)

        cv2.putText(screen,f"Flight : {selected_flight}",
                    (120,160),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,(255,255,255),2)

        cv2.putText(screen,f"Destination : {selected_city}",
                    (120,210),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,(255,255,255),2)

        cv2.putText(screen,"Gate : A12",
                    (120,260),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,(255,255,255),2)

        hover = 180 < cx < 460 and 330 < cy < 400

        clicked, rem = hover_click("seat", hover)

        cv2.rectangle(screen,(180,330),(460,400),
                      (0,180,255) if hover else (120,70,70),-1)

        cv2.putText(screen,"SELECT SEAT",
                    (220,375),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,(255,255,255),2)

        if clicked:
            change_page("seats")

    elif page == "seats":

        screen[:] = (20,20,30)

        cv2.putText(screen,"SELECT SEAT",
                    (180,80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,255,0),2)

        seats = [
            ("12A",150,150),
            ("12B",280,150),
            ("12C",410,150),
            ("13A",150,270),
            ("13B",280,270),
            ("13C",410,270)
        ]

        for seat,x,y in seats:

            hover = x < cx < x+80 and y < cy < y+60

            clicked, rem = hover_click(seat, hover)

            cv2.rectangle(screen,(x,y),(x+80,y+60),
                          (0,180,255) if hover else (70,70,70),-1)

            cv2.putText(screen,seat,(x+10,y+40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,(255,255,255),2)

            if clicked:
                selected_seat = seat
                change_page("boarding")

    elif page == "boarding":

        screen[:] = (15,15,25)

        cv2.rectangle(screen,(80,80),(560,400),
                      (60,60,120),-1)

        cv2.putText(screen,"BOARDING PASS",
                    (170,130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,(255,255,0),2)

        cv2.putText(screen,f"Flight : {selected_flight}",
                    (120,210),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,(255,255,255),2)

        cv2.putText(screen,f"City : {selected_city}",
                    (120,260),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,(255,255,255),2)

        cv2.putText(screen,f"Seat : {selected_seat}",
                    (120,310),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,(255,255,255),2)

        cv2.putText(screen,"Gate : A12",
                    (120,360),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,(255,255,255),2)

    cv2.circle(screen,(cx,cy),35,(255,255,0),1)
    cv2.circle(screen,(cx,cy),25,(255,255,0),2)
    cv2.circle(screen,(cx,cy),12,(255,255,0),cv2.FILLED)

    cv2.imshow("Airport Kiosk V5", screen)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

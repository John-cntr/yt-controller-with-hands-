import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)


last_time = time.time()
last_action = ""

def fingers_up(lm_list):
   
    if not lm_list or len(lm_list) < 21:  
        return []

    fingers = []

  
    fingers.append(1 if lm_list[4][0] > lm_list[3][0] else 0)

   
    tips = [8, 12, 16, 20]
    for tip in tips:
        if len(lm_list) > tip and len(lm_list) > tip - 2:
            fingers.append(1 if lm_list[tip][1] < lm_list[tip - 2][1] else 0)

    return fingers

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            if lm_list:
                fingers = fingers_up(lm_list)

                current_time = time.time()
                if current_time - last_time > 1:  
                    if fingers == [0, 1, 0, 0, 0]:
                        pyautogui.press("l")
                        last_action = "Next Video"
                    elif fingers == [0, 1, 1, 0, 0]:
                        pyautogui.press("j")
                        last_action = "Previous Video"
                    elif fingers == [1, 0, 0, 0, 0]:
                        thumb_tip_y = lm_list[4][1]
                        thumb_base_y = lm_list[3][1]
                        if thumb_tip_y < thumb_base_y:
                            pyautogui.press("volumeup")
                            last_action = "volumeup"

                        else:
                            pyautogui.press("volumedown")
                            last_action = "Volume down"

                    elif fingers == [0, 0, 0, 0, 0]:
                        pyautogui.press("k")
                        last_action = "Pause Video"
                    elif fingers == [1, 1, 1, 1, 1]:
                        pyautogui.press("k")
                        last_action = "Pause Video"
                           
                    
                    last_time = current_time  # Update time

            cv2.putText(img, f'Gesture: {last_action}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
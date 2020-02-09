#For a video of this code in action with a presentation in tandem go to https://www.youtube.com/watch?v=glZ-DQy6r5Q
# the video in the Devpost submission shows the backend whereas this video shows how the code controlled the presentation




import handy
import cv2
import time
import pyautogui

# getting video feed from webcam
cap = cv2.VideoCapture(0)
# capture the hand histogram by placing your hand in the box shown and
# press 'A' to confirm
# source is set to inbuilt webcam by default. Pass source=1 to use an
# external camera.
hist = handy.capture_histogram(source=0)
def handle(comy, comyPrev, comx, comxPrev):
    if comy - comyPrev > 60 and comx - comxPrev > 60:
        print("left Down")
        pyautogui.press("f1")
    elif comy + 60 < comyPrev and comx - comxPrev > 60:
        print("right Down")
        pyautogui.hotkey("1", "0", "enter")
    elif comy - comyPrev > 60 and comx + 60 < comxPrev:
        print("left Up")
        pyautogui.press("esc")
    elif comy + 60 < comyPrev and comx + 60 < comxPrev:
        print("right Up")
        pyautogui.hotkey("1", "enter")
    elif comy - comyPrev > 60:
        print("left")
        pyautogui.press("left")
    elif comy + 60 < comyPrev:
        print("right")
        pyautogui.press("right")
    elif comx - comxPrev > 60:
        print("down")
        pyautogui.press("f2")
    elif comx + 60 < comxPrev:
        print("Up")
        pyautogui.press("f3")
           
def inCenter(x,y):
    if (y>(185) and y<(315)) and (x>(235) and x<(365)):
        return True
    else:
        return False
fire, screen = cap.read()
hand = handy.detect_hand(screen, hist)
com = hand.get_center_of_mass()
   
resetTime =0
prevStatey = com[0]
prevStatex = com[1]
                
while True:
    fire, screen = cap.read()
    if not fire:
        break
    # to block a faces in the video stream, set block=True.
    # if you just want to detect the faces, set block=False
    # if you do not want to do anything with faces, remove this line
    handy.detect_face(screen, block=True)
    # detect the hand
    hand = handy.detect_hand(screen, hist)
    # to get the outline of the hand
    # min area of the hand to be detected = 10000 by default
    custom_outline = hand.draw_outline(
        min_area=10000, color=(0, 255, 255), thickness=2)
    # to get a quick outline of the hand
    quick_outline = hand.outline
    # draw fingertips on the outline of the hand, with radius 5 and color red,
    # filled in.
   
    for fingertip in hand.fingertips:
        cv2.circle(quick_outline, fingertip, 5, (0, 0, 255), -1)
        cv2.circle(quick_outline, (300,250), 50, (255,0,0), 2)
   
    # to get the centre of mass of the hand
    com = hand.get_center_of_mass()
    if com:
        cv2.circle(quick_outline, com, 10, (255, 0, 0), -1)
    cv2.imshow("Handy", quick_outline)

    # display the unprocessed, segmented hand
    # cv2.imshow("Handy", hand.masked)
    # display the binary version of the hand
    # cv2.imshow("Handy", hand.binary)
    k = cv2.waitKey(5)
    # Press 'q' to exit
    if k == ord('q'):
        break

    cv2.circle(quick_outline, (300,250), 50, (255,0,0), 5)
    if resetTime < time.time()-2:
        resetTime = time.time()
        if inCenter(prevStatex,prevStatey):
            if com is not None:
                handle(com[0], prevStatex, com[1], prevStatey)
        if com:
            prevStatex = com[0]
            prevStatey = com[1]
       
   
cap.release()
cv2.destroyAllWindows()

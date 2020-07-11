import pyautogui as pag
import mss, cv2
import numpy as np

# icon postion
left_icon_pos = {'left': 93, 'top': 121, 'width': 70, 'height': 70}
right_icon_pos = {'left': 100, 'top': 540, 'width': 70, 'height': 70}

# buttion position
left_button = {70, 80}
right_button = {70, 80}

pag.PAUSE = 0.8


#  평균값을 구하는 방법 외의 알고리즘 -> Histogram, KMeans 
def computer_icon_type(img):
    # img 변수의 0번 1번 축의 평균값을 구함
    mean = np.mean(img, axis=(0, 1))
    result = None

    if mean[0] > 50 and mean[0] < 55 and mean[1] > 50 and mean[1] < 55 and mean[2] > 50 and mean[2] < 55:
        result = 'BOMB'
    elif mean[0] > 250 and mean[0] > 85 and mean[1] > 110 and mean[2] < 220:
        result = 'SWORD'
    elif mean[0] > 100 and mean[0] < 130 and mean[1] > 150 and mean[1] < 200 and mean[2] > 90 and mean[2] < 110:
        result = 'PROSION'
    elif mean[0] > 210 and mean[0] < 230 and mean[1] > 200 and mean[1] < 255 and mean[2] > 120 and mean[2] < 135:
        result = 'JEWEL'

    return result


# take screenshot
with mss.mss() as sct:
    left_img = np.array(sct.grab(left_icon_pos))[:, :, :3]
    right_img = np.array(sct.grab(right_icon_pos))[:, :, :3]

    # cv2.imshow('left_img', left_img)
    # cv2.imshow('right_img', right_img)
    # cv2.waitKey(0)

    left_icon = computer_icon_type(left_img)
    right_icon = computer_icon_type(right_img)

    if left_icon == "SWORD" and (right_icon == "BOMB" or right_icon == "POSTION"):
        print("TAP LEFT")
        click(left_button)
    elif left_icon == "SWORD" and (left_icon == "BOMB" or right_icon == "POSTION"):
        print("TAP RIGHT")
        click(right_button)
    elif left_icon == "JEWEL" and (right_icon == "JEWEL" or right_icon == "FEVER"):
        print("FEVER")
        click(left_button)
        click(right_button)
    else:
        print("FAIL")


def click(coords):
    pag.moveTo(x=coords[0], y=coords[1], duration=0.0)
    pag.mouseDown()
    pag.mouseUp


while True:
    x, y = pag.position()
    postion_str = 'X:' + str(x) + ' Y:' + str(y)
    print(postion_str)

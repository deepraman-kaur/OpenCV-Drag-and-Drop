import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8)

class DragImg():
    def __init__(self,path,posOrigin,imgType):

        self.posOrigin = posOrigin
        self.imgType = imgType
        self.path = path

        if self.imgType == "png":
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        self.size = self.img.shape[:2]

    def update(self,cursor):
        ox, oy = self.posOrigin
        h, w = self.size

        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2



# img1 =  cv2.imread("ImagesJPG/1.jpg")
# ox,oy = 200,200

path = "ImagesJPG"
myList = os.listdir(path)
# print(myList)

listImg = []

for x,pathImg in enumerate(myList):
    if "png" in pathImg:
        imgType = 'png'
    else:
        imgType = 'jpg'
    listImg.append(DragImg(f'{path}/{pathImg}',[50+x*300,50],imgType))

# print(len(listImg))

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    # print(f"hands  {hands}")
    # print(f"img  {img}")

    if hands:
        lmList = hands[0]['lmList']

        length, info, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)
        # print(f" length is {length}")

        if length<60:
            cursor = lmList[8]
            for imgObject in listImg:
                imgObject.update(cursor)

        # print(f"lmList[8] is {lmList[8]} \n")
        # print(f"cursor {cursor[0]} and {cursor[1]}")


    '''draw for single jpg
    h,w , _ = img1.shape
    img[oy:oy+h, ox:ox+w] = img1'''

    '''draw for single png
    h,w , _ = img1.shape
    img = cvzone.overlayPNG(img, img1, [ox, oy])'''

    try:

        for imgObject in listImg:

            h, w = imgObject.size
            ox, oy = imgObject.posOrigin

            if imgObject.imgType == 'png':
                img = cvzone.overlayPNG(img, img1, [ox, oy])
            else:
                img[oy:oy+h, ox:ox+w] = imgObject.img


    except:

        pass

    cv2.imshow("Image", img)
    cv2.waitKey(1)

cv2.destroyAllWindows()
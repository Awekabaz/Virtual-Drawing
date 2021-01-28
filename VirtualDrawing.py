import cv2
import numpy as np

flagList = [0,1]
globCounter = 0
drawing = flagList[0]
mode, connect = True, False
drawPath = []  # x ,y, color, size
pointsRectangle = [] # poits for drawing rectangle

#windowWidth, windowHeight = 500, 300
# sequence: hMin, sMin, vMin, hMax, sMax, vMax
deepGreen = [55,79,0,117,255,255]
lightRed = [78,133,104,179,255,255]
colorList = [deepGreen, lightRed]

#Coresponding color for drawing
green = [0,255,0]
red = [0,0,255]
colorDrawing = [green, red]

capture = cv2.VideoCapture(0)
capture.set(3, 500)
capture.set(4, 400)

def fixPoint(points, color):
    for point in points:
        cv2.circle(imageOutput, (point[0], point[1]), 10, colorDrawing[point[2]], cv2.FILLED)

def drawRectangle(points, colorDrawing):
    color = colorDrawing[points[0][2]]
    for i in range(len(points)-1):
        cv2.line(imageOutput, (points[i][0], points[i][1]), (points[i+1][0], points[i+1][1]), color, 5)

    cv2.line(imageOutput, (points[-1][0], points[-1][1]), (points[0][0], points[0][1]), color, 5)


def drawLine(points, colorValue, flag):
    if flag:
        for point in points:
            cv2.circle(imageOutput, (point[0], point[1]), 5*point[3], colorDrawing[point[2]], cv2.FILLED)
            cv2.circle(imageOutput, (point[0]+2, point[1]+2), 2 * point[3], colorDrawing[point[2]], cv2.FILLED)
            cv2.circle(imageOutput, (point[0]+2, point[1]-2), 2 * point[3], colorDrawing[point[2]], cv2.FILLED)
            cv2.circle(imageOutput, (point[0]-2, point[1]+2), 2 * point[3], colorDrawing[point[2]], cv2.FILLED)
            cv2.circle(imageOutput, (point[0]-2, point[1]-2), 2 * point[3], colorDrawing[point[2]], cv2.FILLED)

def getCon(image):
    x, y, width, height, ratioSize = 0,0,0,0,0
    cons, hrhy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in cons:
        area = cv2.contourArea(contour)
        if area>7000:
            cv2.drawContours(imageOutput, contour, -1, (0, 0, 0), 5)
            perimeter = cv2.arcLength(contour,True)
            corners = cv2.approxPolyDP(contour, 0.01*perimeter, True)
            x, y, width, height = cv2.boundingRect(corners)
            ratioSize = round((area // 10000))
            #print(ratioSize)
    return x+width //2, y, ratioSize


def colorDetect(image, colors):
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    pointsList = []  # x ,y, color, size
    schet = 0
    for colorPars in colors:
        lowerLimit = np.array(colorPars[:3])
        upperLimit = np.array(colorPars[3:6])
        mask = cv2.inRange(imgHSV, lowerLimit, upperLimit)
        xCoord, yCoord, ratioSize = getCon(mask)

        cv2.circle(imageOutput, (xCoord, yCoord), 5*ratioSize, colorDrawing[schet], cv2.FILLED)
        if xCoord!=0 and yCoord!=0:
            pointsList.append([xCoord,yCoord,schet, ratioSize])
        schet +=1
    return pointsList

while True:
    success, image = capture.read()
    imageOutput = image.copy()
    blur = cv2.GaussianBlur(image, (5,5), 0)
    pointsList = colorDetect(blur, colorList)

    if cv2.waitKey(1) & 0xFF == ord('p'):
        drawPath = []
        pointsRectangle = []

    if cv2.waitKey(1) & 0xFF == ord('r'):
        pointsRectangle.append(pointsList[-1])
    fixPoint(pointsRectangle, colorDrawing)

    if cv2.waitKey(1) & 0xFF == ord('t'):
        connect = not connect
    if connect:
        drawRectangle(pointsRectangle, colorDrawing)

    if cv2.waitKey(1) & 0xFF == ord('d'):
        globCounter += 1
        drawing = flagList[globCounter%len(flagList)]
        drawPath = []

    if pointsList:
        for obj in pointsList:
            drawPath.append(obj)
    if drawPath:
        drawLine(drawPath, colorDrawing, drawing)

    cv2.imshow('Result', imageOutput)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
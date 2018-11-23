import sys
import json
import numpy as np
import cv2 as cv

FONT = cv.FONT_HERSHEY_SIMPLEX
BBOX_COLOR = (0,255,0)
MARKER_COLOR = (0,0,255)
FEATURES = [
    # MOUTH
    ["LOWER_LIP", "MOUTH_LEFT", "UPPER_LIP", "MOUTH_RIGHT"],
    ["NOSE_BOTTOM_LEFT", "NOSE_BOTTOM_CENTER", "NOSE_BOTTOM_RIGHT", "MIDPOINT_BETWEEN_EYES"]
]

def drawRect(rect, img):
    # print(rect)
    p1 = rect["vertices"][0]
    p2 = rect["vertices"][2]
    cv.rectangle(img, (p1["x"],p1["y"]), (p2["x"],p2["y"]), BBOX_COLOR, 2)

def drawLandmark(lm, img, text = True):
    # print(lm)
    x = int(lm["position"]["x"])
    y = int(lm["position"]["y"])
    cv.circle(img, (x,y), 2, MARKER_COLOR, -1)
    if text:
        cv.putText(img,lm["type"],(x+5,y+2), FONT, 0.3,(255,255,255), 1 ,cv.LINE_AA)

def getLandmarkPoint(landmarks, id):
    for lm in landmarks:
        if lm["type"] == id:
            pos = lm["position"]
            return [pos["x"], pos["y"]]

def drawFeature(feature, landmarks, img):
    poly = []
    for item in feature:
        p = getLandmarkPoint(landmarks, item)
        # print(p)
        poly.append(p)
    # print(poly)
    pts = np.array(poly, np.int32)
    pts = pts.reshape((-1,1,2))
    cv.polylines(img, [pts], True, MARKER_COLOR)

basename = sys.argv[1]
with open(basename + '.json') as json_data:
    d = json.load(json_data)
    # print(d)

#Read Image
img = cv.imread(basename + '.png')
print(img.shape)

outerBB = d["responses"][0]["faceAnnotations"][0]["boundingPoly"]
drawRect(outerBB, img)

innerBB = d["responses"][0]["faceAnnotations"][0]["fdBoundingPoly"]
drawRect(innerBB, img)

landmarks = d["responses"][0]["faceAnnotations"][0]["landmarks"]
for l in landmarks:
    drawLandmark(l, img, True)

# FEATURES
for f in FEATURES:
    drawFeature(f, landmarks, img)

# crop
p1 = outerBB["vertices"][0]
p2 = outerBB["vertices"][2]
img = img[ p1["y"]:p2["y"], p1["x"]:p2["x"]]

# scale
r = 800.0 / img.shape[1]
dim = (800, int(img.shape[0] * r))
img = cv.resize(img, dim, interpolation = cv.INTER_AREA)

#Display Image
cv.imshow('image', img)
cv.waitKey(0)
cv.destroyAllWindows()

import sys
import json
import cv2 as cv

FONT = cv.FONT_HERSHEY_SIMPLEX
BBOX_COLOR = (0,255,0)
MARKER_COLOR = (0,0,255)

def drawRect(rect, img):
    # print(rect)
    p1 = rect["vertices"][0]
    p2 = rect["vertices"][2]
    cv.rectangle(img, (p1["x"],p1["y"]), (p2["x"],p2["y"]), BBOX_COLOR, 2)

def drawLandmark(lm, img):
    # print(lm)
    x = int(lm["position"]["x"])
    y = int(lm["position"]["y"])
    cv.circle(img, (x,y), 2, MARKER_COLOR, -1)
    cv.putText(img,lm["type"],(x+5,y+2), FONT, 0.3,(255,255,255), 1 ,cv.LINE_AA)

basename = sys.argv[1]
with open(basename + '.json') as json_data:
    d = json.load(json_data)
    print(d)

#Read Image
img = cv.imread(basename + '.png')
print(img.shape)

bbox = d["responses"][0]["faceAnnotations"][0]["boundingPoly"]
drawRect(bbox, img)

bbox = d["responses"][0]["faceAnnotations"][0]["fdBoundingPoly"]
drawRect(bbox, img)

landmarks = d["responses"][0]["faceAnnotations"][0]["landmarks"]
for l in landmarks:
    drawLandmark(l, img)

# scale
r = 1600.0 / img.shape[1]
dim = (1600, int(img.shape[0] * r))
# img = cv.resize(img, dim, interpolation = cv.INTER_AREA)

#Display Image
cv.imshow('image',img)
cv.waitKey(0)
cv.destroyAllWindows()

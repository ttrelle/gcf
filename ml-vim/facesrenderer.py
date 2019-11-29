from PIL import Image, ImageDraw
from basicrenderer import drawRect, processAnnotations
from google.cloud.vision import types

BBOX_COLOR = (255, 255, 255)
MARKER_COLOR = (255, 0, 0)
LINE_WIDTH = 3

FEATURES = [
    # Mouth
    (True, ["LOWER_LIP", "MOUTH_LEFT", "UPPER_LIP", "MOUTH_RIGHT"]),
    # Nose
    (True, ["NOSE_BOTTOM_LEFT", "NOSE_BOTTOM_CENTER", "NOSE_BOTTOM_RIGHT", "MIDPOINT_BETWEEN_EYES"]),

    # left eyebrow
    (False, ["LEFT_OF_LEFT_EYEBROW", "LEFT_EYEBROW_UPPER_MIDPOINT", "RIGHT_OF_LEFT_EYEBROW"]),
    # left eye
    (True, ["LEFT_EYE_TOP_BOUNDARY", "LEFT_EYE_RIGHT_CORNER", "LEFT_EYE_BOTTOM_BOUNDARY", "LEFT_EYE_LEFT_CORNER"]),

    # right eyebrow
    (False, ["LEFT_OF_RIGHT_EYEBROW", "RIGHT_EYEBROW_UPPER_MIDPOINT", "RIGHT_OF_RIGHT_EYEBROW"]),
    # right eye
    (True, ["RIGHT_EYE_TOP_BOUNDARY", "RIGHT_EYE_RIGHT_CORNER", "RIGHT_EYE_BOTTOM_BOUNDARY", "RIGHT_EYE_LEFT_CORNER"]),

    # chin
    (False, ["LEFT_EAR_TRAGION", "CHIN_LEFT_GONION", "CHIN_GNATHION", "CHIN_RIGHT_GONION", "RIGHT_EAR_TRAGION"])
]

def processFaces(faceAnnotations, img):
    return processAnnotations(faceAnnotations, processFace, img)

def processFace(faceAnnotations, canvas, size):
    # bounding boxes
    drawRect(canvas, faceAnnotations.bounding_poly.vertices)
    drawRect(canvas, faceAnnotations.fd_bounding_poly.vertices)

    landmarks = faceAnnotations.landmarks
    for l in landmarks:
        drawLandmark(canvas, l, False)

    # FEATURES
    for f in FEATURES:
        drawFeature(canvas, f, landmarks) 

def drawLandmark(draw, lm, text = True):
    # print(lm)
    x = int(lm.position.x)
    y = int(lm.position.y)
    draw.ellipse(xy=[(x-1,y-1),(x+2, y+1)], fill = MARKER_COLOR, width=LINE_WIDTH)
    if text:
        draw.text(xy= (x+5,y+2), text = str(lm.type), fill = BBOX_COLOR)

def getLandmarkPoint(landmarks, id):
    for lm in landmarks:
        if lm.type == types.image_annotator_pb2._FACEANNOTATION_LANDMARK_TYPE.values_by_name[id].number:
            pos = lm.position
            return (pos.x, pos.y)

def drawFeature(canvas, feature, landmarks):
    closePoly, featureList = feature
    poly = []
    for item in featureList:
        poly.append(getLandmarkPoint(landmarks, item))

    if closePoly:
        poly.append(getLandmarkPoint(landmarks, featureList[0]))
        
    canvas.line(xy=poly, fill=MARKER_COLOR, width=LINE_WIDTH)

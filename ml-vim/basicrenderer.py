from PIL import Image, ImageDraw

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

def processImage(name, data, raw = None):
    # Image
    if raw is None:
        img = Image.open(name)
    else:
        img = Image.open(raw)
        
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    outerBB = data["responses"][0]["faceAnnotations"][0]["boundingPoly"]
    drawRect(draw, outerBB)

    innerBB = data["responses"][0]["faceAnnotations"][0]["fdBoundingPoly"]
    drawRect(draw, innerBB)

    landmarks = data["responses"][0]["faceAnnotations"][0]["landmarks"]
    for l in landmarks:
        drawLandmark(draw, l, False)

    # FEATURES
    for f in FEATURES:
        drawFeature(draw, f, landmarks)

    return img

def drawRect(draw, rect):
    p1 = rect["vertices"][0]
    p2 = rect["vertices"][2]
    draw.rectangle( xy = [(p1["x"],p1["y"]), (p2["x"],p2["y"])], outline = BBOX_COLOR, width= LINE_WIDTH)

def drawLandmark(draw, lm, text = True):
    # print(lm)
    x = int(lm["position"]["x"])
    y = int(lm["position"]["y"])
    draw.ellipse(xy=[(x-1,y-1),(x+2, y+1)], fill = MARKER_COLOR, width=LINE_WIDTH)
    if text:
        draw.text(xy= (x+5,y+2), text = lm["type"], fill = BBOX_COLOR)

def getLandmarkPoint(landmarks, id):
    for lm in landmarks:
        if lm["type"] == id:
            pos = lm["position"]
            return (pos["x"], pos["y"])

def drawFeature(draw, feature, landmarks):
    closePoly, featureList = feature
    poly = []
    for item in featureList:
        poly.append(getLandmarkPoint(landmarks, item))

    if closePoly:
        poly.append(getLandmarkPoint(landmarks, featureList[0]))
        
    draw.line(xy=poly, fill=MARKER_COLOR, width=LINE_WIDTH)
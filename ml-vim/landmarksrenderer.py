from PIL import Image, ImageDraw
from basicrenderer import drawRect, processAnnotations

def processLandmarks(name, landmarkAnnotations, raw = None):
    return processAnnotations(name, landmarkAnnotations, processLandmark, raw)

def processLandmark(data, canvas, size):
    drawRect(canvas, data["boundingPoly"]["vertices"], data["description"])

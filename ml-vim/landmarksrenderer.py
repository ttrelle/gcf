from PIL import Image, ImageDraw
from basicrenderer import drawRect, processAnnotations

def processLandmarks(landmarkAnnotations, img):
    return processAnnotations(landmarkAnnotations, processLandmark, img)

def processLandmark(data, canvas, size):
    drawRect(canvas, data.bounding_poly.vertices, data.description)

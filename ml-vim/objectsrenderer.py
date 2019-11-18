from PIL import Image, ImageDraw
from basicrenderer import drawRect, processAnnotations

def processObjects(name, objectAnnotations, raw = None):
    return processAnnotations(name, objectAnnotations, processObject, raw)

def processObject(data, canvas, size):
    vertices = data["boundingPoly"]["normalizedVertices"]
    for v in vertices:
        v["x"] *= size[0]
        v["y"] *= size[1]
    drawRect(canvas, vertices, data["name"])
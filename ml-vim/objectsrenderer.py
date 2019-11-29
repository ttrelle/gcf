from PIL import Image, ImageDraw
from basicrenderer import drawRect, processAnnotations

def processObjects(objectAnnotations, img):
    return processAnnotations(objectAnnotations, processObject, img)

def processObject(data, canvas, size):
    vertices = data.bounding_poly.normalized_vertices
    # scaling normalized coordinates
    for v in vertices:
        v.x *= size[0]
        v.y *= size[1]
    drawRect(canvas, vertices, data.name)
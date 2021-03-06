from PIL import Image, ImageDraw

BBOX_COLOR = (255, 255, 255)
LINE_WIDTH = 3

def drawRect(canvas, vertices, text = None):
    p1 = vertices[0]
    p2 = vertices[2]
    canvas.rectangle( xy = [(p1.x,p1.y), (p2.x,p2.y)], outline = BBOX_COLOR, width= LINE_WIDTH)
    if text:
        # draw in left upper corner
        x = int(p1.x)
        y = int(p1.y)
        canvas.text(xy= (x+5,y+2), text = text, fill = BBOX_COLOR)

def processAnnotations(annotations, processAnnotation, img):

    canvas = ImageDraw.Draw(img)

    # iterate annotation
    for annotation in annotations:
        processAnnotation(annotation, canvas, img.size)

    return img
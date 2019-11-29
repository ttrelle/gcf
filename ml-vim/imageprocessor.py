import io
from google.cloud import vision
from PIL import Image

from facesrenderer import processFaces 
from landmarksrenderer import processLandmarks
from objectsrenderer import processObjects

vision_client = vision.ImageAnnotatorClient()

def process_image(buffer):
    # vision API call
    response = vision_client.annotate_image({
        'image': {'content': buffer },
        'features': [
            {'type': vision.enums.Feature.Type.FACE_DETECTION},
            {'type': vision.enums.Feature.Type.OBJECT_LOCALIZATION}
        ],
    })

    img = None
    if response is not None:
        img = Image.open(io.BytesIO(buffer))
        img = img.convert("RGB")

        if response.face_annotations is not None:
            img = processFaces(response.face_annotations, img)

        if response.localized_object_annotations is not None:
            img = processObjects(response.localized_object_annotations, img)

        if response.landmark_annotations is not None:
            img = processLandmarks(response.landmark_annotations, img)            

    return img
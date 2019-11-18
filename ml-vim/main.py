import io
import sys
import json
from facesrenderer import processFaces 
from landmarksrenderer import processLandmarks
from objectsrenderer import processObjects

input_file = sys.argv[1]
meta_file = sys.argv[2]
output_file = sys.argv[3]

# read input image
with open(input_file, 'rb') as fp:
    rawImage = io.BytesIO(fp.read())
# read JSON meta data
with open(meta_file) as json_data:
    metadata = json.load(json_data)

# process Image
img = None
if "responses" in metadata and metadata["responses"][0] is not None:

    # render faces    
    if "faceAnnotations" in metadata["responses"][0]:
        img = processFaces(input_file, metadata["responses"][0]["faceAnnotations"], rawImage)

    if "landmarkAnnotations" in metadata["responses"][0]:
        img = processLandmarks(input_file, metadata["responses"][0]["landmarkAnnotations"], rawImage)

    if "localizedObjectAnnotations" in metadata["responses"][0]:
        img = processObjects(input_file, metadata["responses"][0]["localizedObjectAnnotations"], rawImage)


    # TODO: add more renderers here

    # write output image
    if img:
        img.save(output_file, optimize = True)
        # won't work since last MacOS update
        # img.show()
import io
import sys
import json
from facesrenderer import processFaces 

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
img = processFaces(input_file, metadata, rawImage)

# crop
#p1 = outerBB["vertices"][0]
#p2 = outerBB["vertices"][2]
#img = img[ p1["y"]:p2["y"], p1["x"]:p2["x"]]

# scale
#r = 800.0 / img.shape[1]
#dim = (800, int(img.shape[0] * r))
#img = cv.resize(img, dim, interpolation = cv.INTER_AREA)

# write output image
img.save(output_file, optimize = True)
img.show()


import io
import sys
import json
from addfacedata import processImage 

basename = sys.argv[1]
with open(basename + '.json') as json_data:
    metadata = json.load(json_data)

with open(basename + '.png', 'rb') as fp:
    rawImage = io.BytesIO(fp.read())

#Read Image
img = processImage(basename + ".png", metadata, rawImage)

# crop
#p1 = outerBB["vertices"][0]
#p2 = outerBB["vertices"][2]
#img = img[ p1["y"]:p2["y"], p1["x"]:p2["x"]]

# scale
#r = 800.0 / img.shape[1]
#dim = (800, int(img.shape[0] * r))
#img = cv.resize(img, dim, interpolation = cv.INTER_AREA)

#Display Image
img.show()

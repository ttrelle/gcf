import io
import sys

from imageprocessor import process_image

input_file = sys.argv[1]
output_file = sys.argv[2]

# read input image
with open(input_file, 'rb') as fp:
    buffer = io.BytesIO(fp.read())

# process image
img = process_image(buffer)

# write output image
if img:
    img.save(output_file, optimize = True)
    print(f"output written to: {output_file}")
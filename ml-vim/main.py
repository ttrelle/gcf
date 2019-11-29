import io

from google.cloud import storage
from PIL import Image
from imageprocessor import process_image

OUT_BUCKET = 'vision-test-out'
OUTPUT_FORMAT = 'png'

storage_client = storage.Client()

def on_storage_event(event, context):
	bucket_name = event['bucket']
	file_name = event['name']

    # read image buffer from inj bucket
	buffer = read_image_buffer(bucket_name, file_name)  

    # process image
	img = process_image(buffer)

	# write annotated image to out bucket
	write_image(img, OUT_BUCKET, file_name)

def read_image(bucket_name, file_name):
	return Image.open(read_image_buffer(bucket_name, file_name))

def read_image_buffer(bucket_name, file_name):
	blob = get_blob(bucket_name, file_name)
	return blob.download_as_string()

def write_image(img, bucket_name, file_name):
	blob = get_blob(bucket_name, file_name)
	buffer = io.BytesIO()
	img.save(buffer, OUTPUT_FORMAT, optimize = True)
	blob.upload_from_string(buffer.getvalue(), f"image/{OUTPUT_FORMAT}")
       
def get_blob(bucket_name, file_name):
	bucket = storage_client.get_bucket(bucket_name)
	blob = bucket.blob(file_name)
	return blob

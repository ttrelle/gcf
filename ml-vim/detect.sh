FILE=$1
BASE="${FILE%.*}"
EXT="${FILE##*.}"

gcloud ml vision detect-faces $FILE > ${BASE}.json
python ./main.py $FILE ${BASE}.json ${BASE}-faces.jpg
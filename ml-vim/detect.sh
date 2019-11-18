MODE=$1
FILE=$2
BASE="${FILE%.*}"
EXT="${FILE##*.}"

gcloud ml vision detect-$MODE $FILE > ${BASE}.json
python ./main.py $FILE ${BASE}.json ${BASE}-${MODE}.jpg
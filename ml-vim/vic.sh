MODE=$1
FILE=$2
BASE="${FILE%.*}"
EXT="${FILE##*.}"

python3 ./vic.py $FILE ${BASE}-${MODE}.${EXT}
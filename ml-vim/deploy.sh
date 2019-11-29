#!/bin/sh

# use your bucket name here
gcloud functions deploy ml-vim-1 \
  --entry-point=on_storage_event \
  --runtime=python37 \
  --trigger-resource=vision-test-in \
  --trigger-event=google.storage.object.finalize

#!/bin/sh

gcloud functions deploy aes-1 \
  --entry-point=analyse_entity_sentiment \
  --trigger-resource=nlp-test-in \
  --trigger-event=google.storage.object.finalize

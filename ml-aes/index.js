const Storage = require('@google-cloud/storage');
const languageApi = require('@google-cloud/language');

const OUT_BUCKET_NAME = "nlp-test-out";

// Storage API
const storage = new Storage();
const outputBucket = storage.bucket(OUT_BUCKET_NAME);

// Language API
const client = new languageApi.LanguageServiceClient();

function gcsUri(bucket, file) {
  return `gs://${bucket}/${file}`;
}

function outputFilename(inputFilename) {
  return inputFilename.replace(".txt", "-results.json");
}

/**
 * Triggered from a message on a Cloud Storage bucket.
 *
 * @param {!Object} event The Cloud Functions event.
 * @param {!Function} The callback function.
 */
exports.analyse_entity_sentiment = function(event, callback) {
  const data = event.data;
  const inputFileUri = gcsUri(data.bucket, data.name);
  const outFilename = outputFilename(data.name);

  console.log('Processing text from: ' + inputFileUri);
  const aesRequest = {
    gcsContentUri: inputFileUri,
    type: 'PLAIN_TEXT'
  };

  // Call to Language API
  client
    .analyzeEntitySentiment({document: aesRequest})
    .then(results => {
      const outputFile = outputBucket.file(outFilename);
      outputFile.save(JSON.stringify(results));
      console.info('Text analysis results writtten to: ' + gcsUri(OUT_BUCKET_NAME,outFilename));
	  callback();
    });
}

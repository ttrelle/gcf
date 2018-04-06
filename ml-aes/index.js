const OUT_BUCKET_NAME = "nlp-test-out";

// Storage API
const storage = require('@google-cloud/storage')();
const outputBucket = storage.bucket(OUT_BUCKET_NAME);

// Language API
const language = require('@google-cloud/language');
const client = new language.LanguageServiceClient();

/**
 * Triggered from a message on a Cloud Storage bucket.
 *
 * @param {!Object} event The Cloud Functions event.
 * @param {!Function} The callback function.
 */
exports.analyse_entity_sentiment = (event, callback) => {
  const data = event.data;
  const inputFileUri = inputFileGcsUri(data);
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
      console.info('Text analysis results writtten to: gs://' + OUT_BUCKET_NAME + '/' + outFilename);
    })
    .then(() =>{
      callback();
    }).
    catch(err => {
      console.error('ERROR: ' + err);
      callback(err);
    });
};

function inputFileGcsUri(data) {
  return "gs://" + data.bucket + "/" + data.name;
}

function outputFilename(inputFilename) {
  return inputFilename.replace(".txt", "-results.json");
}

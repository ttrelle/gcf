# Google Cloud Function for Entity Sentiment Analysis

This Cloud Function is implemented in JavaScript.

It is triggered by file uploads to a Storage bucket *nlp-test-in* and performs an entity sentiment analysis of using the plain text content of the uploaded file.

The analysis result is stored in another bucket named *nlp-test-out*.

![Analyze Entity Sentiment](img/gcf_ml_aes.png)


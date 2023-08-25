const uploader = require('youtube-videos-uploader');

// Retrieve the video_params from the command-line arguments
const [videoParamsJSON] = process.argv.slice(2);
const videoParams = JSON.parse(videoParamsJSON);

// Destructure the video_params object
const { file, title, description, privacyStatus } = videoParams;

// Set up your authentication credentials and other options
const credentials = { email: process.env.EMAIL, pass: process.env.PASSWORD };
const video = {
  path: file,
  title,
  description,
  language: 'english',
  skipProcessingWait: true,
  onProgress: (progress) => {
    console.log('progress', progress);
  },
  uploadAsDraft: false,
  isAgeRestriction: false,
  isNotForKid: false,
  publishType: privacyStatus.toUpperCase()
};

uploader.upload (credentials, [video], {headless:true}).then(console.log)

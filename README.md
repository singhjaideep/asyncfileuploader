# asyncfileuploader
Async file uploader using tornado

## Detailed Description
This simple file uploader uses tornado for demostrating some async operations using gen.coroutine. When the application is accessed through localhost:8080 FormHandler's GET method is called and form is rendered. User selects and uploads the file. In the FormHandler POST method, It checks for file size and file type. Then computes SHA hash for the file, and checks if the same hash already exists. If it does, it displays the file info for that file. If not, It triggers a coroutine to calculate statistics about that file, stores them and writes it to '/uploaded' folder on disk. Then it renders an xml stating the status (new/exists), filename, number of words and frequency along with each unique word.

## How to run
Requires Python

Uses tornado and nltk library (for splitting words)
Run:
- pip install tornado
- pip install -U pyyaml nltk

Then application can be run using:
python uploadedfile.py

Now its visible via browser at localhost:8888

## Run tests
Tested on Python 2.7, tornado 3.2.1, nltk 2.0.4 and Mozilla Firefox 28

## Licence
Apache

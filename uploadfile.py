from tornado import ioloop, web, gen
from hashlib import sha224
from nltk import word_tokenize
'''
TODO:
-refactor
-correct HTTP REST responses like localhost:8888/uploaded/HASH?mimetype=application/xml
-application design, test coverage and readability
-Test coverage needs success and failure conditions
-README
'''

filestatsdict = {}
    
class FormHandler(web.RequestHandler):
    def get(self, ):
        self.render('index.html')
  
    @gen.coroutine
    def post(self, ):
        global filestatsdict
        inputfile = self.request.files['fileupload'][0] #collect the file
        filetype = inputfile['content_type']
        filesize = len(inputfile['body'])
        if filesize > 10485760: #check for 10 MB
            self.write('<html><h2>File is larger than 10 MB</h2></html>')
            self.finish()            
        if filetype != 'text/plain':
            self.write('<html><h2>File type not supported</h2></html>')
            self.finish()
        hashed = sha224(inputfile['body']).hexdigest() #find hash.. should I use uuid?
        status = 'Exists' #default
        if hashed not in filestatsdict.keys():
            status='New' #new file!
            yield self._calcStats(inputfile=inputfile, hashed=hashed) #calcStats
            yield self._write(outputfile=inputfile) #write file
        numberofwords = filestatsdict[hashed]
        self.set_header("Content-Type", "text/xml")
        self.render('uploaded.xml', status=status, filename=inputfile['filename'], numberofwords=str(len(numberofwords)), words=numberofwords)

    @gen.coroutine
    def _calcStats(self, inputfile=None, hashed=None):
        global filestatsdict
        worddict = {}
        sentence = word_tokenize(inputfile['body'])
        for word in sentence:
            word = ''.join(e for e in word if e.isalnum()) #removing anything thats not alphanumeric
            if word == '':
                pass
            elif word in worddict.iterkeys():
                worddict[word] += 1
            else:
                worddict[word] = 1
        filestatsdict[hashed] = worddict

    @gen.coroutine
    def _write(self, outputfile=None):
        fileio = open('uploads/'+outputfile['filename'], 'w')
        fileio.write(outputfile['body'])
        fileio.close()

application = web.Application([
    (r"/", FormHandler),
    (r"/uploaded/", FormHandler),
], debug=True)

if __name__ == '__main__':
    application.listen(8888)
    ioloop.IOLoop.instance().start()
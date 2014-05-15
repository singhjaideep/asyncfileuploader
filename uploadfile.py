import tornado.ioloop
import tornado.web
import tornado.gen
import hashlib

'''
TODO:
-refactor
-check for size
-async + correct HTTP REST responses
-count words better
-application design, test coverage and readability
-Test coverage needs success and failure conditions
-README
'''

filestatsdict = {}

class MainHandler(tornado.web.RequestHandler):
    def get(self, ):
        self.write('Hello world')
    
class MyFormHandler(tornado.web.RequestHandler):
    def get(self, ):
        self.write('<html><body><form action="/myform/" enctype="multipart/form-data" method="post">'
                   '<input type="text" name="message"><br>'
                   '<input type="file" name="fileupload" accept="text/plain">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
        
    def _calcHash(self, filez):
        print 'in _calcHash'
        return hashlib.sha224(filez).hexdigest()
    
    @tornado.gen.coroutine
    def _calcStats(self, filez):
    #The number of words in the file.
    #The occurrences of each word, as some words may have been repeated.
        print 'in _calcStats'
        global filestatsdict
        worddict = {}
        hashed = self._calcHash(filez['body'])
        if hashed not in filestatsdict.keys():
            for word in filez['body'].split():
                if word in worddict.iterkeys():
                    worddict[word] += 1
                else:
                    worddict[word] = 1
        filestatsdict[hashed] = worddict
        return
    
    def _write(self, filez=None):
        print 'in _write'
        fileio = open('uploads/'+filez['filename'], 'w')
        fileio.write(filez['body'])
        fileio.close()
    
    #@tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, ):
        print 'in post'
        inputfile = self.request.files['fileupload'][0]
        filename = inputfile['filename']
        
        response  = yield self._calcStats(filez=inputfile)
        print 'returning in post'
        print response
        hashish = filestatsdict[self._calcHash(inputfile['body'])]
        self._write(inputfile)
        
        self.set_header("Content-Type", "text/xml")
        self.write('<?xml version="1.0" encoding="UTF-8"?>'
                   '<response status="OK"><filename>'+filename+'</filename>'
                   '<NumberOfWords>'+str(len(hashish))+'</NumberOfWords>'
                   '<words>Fill this</words></response>')
        self.finish()
            


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/myform/", MyFormHandler),
    (r"/upload", MyFormHandler)
])


if __name__ == '__main__':
    print 'Listening at localhost:8888'
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
import tornado.ioloop
import tornado.web
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

def calcHash(filez):
    return hashlib.sha224(filez).hexdigest()

def calcStats(filez):
    #The number of words in the file.
    #The occurrences of each word, as some words may have been repeated.
    global filestatsdict
    worddict = {}
    hashed = calcHash(filez)
    if hashed in filestatsdict.keys():
        return False
    for word in filez.split():
        if word in worddict.iterkeys():
            worddict[word] += 1
        else:
            worddict[word] = 1
    filestatsdict[hashed] = worddict
    return True


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
    
    def post(self, ):
        filez = self.request.files['fileupload'][0]
        filename = filez['filename']
        
        if calcStats(filez['body']):
            fileio = open('uploads/'+filename, 'w')
            fileio.write(filez['body'])
            
            self.set_header("Content-Type", "text/xml")
            self.write('<?xml version="1.0" encoding="UTF-8"?>'
                       '<response status="uploaded"><message>'+filename+' uploaded</message>'
                       '<NumberOfWords>'+str(len(filestatsdict[calcHash(filez['body'])]))+'</NumberOfWords>'
                       '<words>Fill this</words></response>')
        else:
            self.set_header("Content-Type", "text/xml")
            self.write('<?xml version="1.0" encoding="UTF-8"?>'
                       '<response status="exists"><message>'+filename+' already exists</message>'
                       '<NumberOfWords>'+str(len(filestatsdict[calcHash(filez['body'])]))+'</NumberOfWords>'
                       '<words>Fill this</words></response>')


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/myform/", MyFormHandler),
    (r"/upload", MyFormHandler)
])


if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
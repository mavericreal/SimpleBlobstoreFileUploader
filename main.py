#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import blobstore
from os import path
from google.appengine.ext.webapp import blobstore_handlers
import urllib
import urllib2
import logging

KEY_BOUNDARY='BOUNDARY--'

class FormHandler(webapp.RequestHandler):
	def get(self):
		temp = path.join(path.dirname(__file__),"templates/main.html")
		html = template.render(temp,{}) 
		self.response.out.write(html)
		
class Blobstore(webapp.RequestHandler):
	def get(self):
		upload_url = blobstore.create_upload_url('/upload/')
		temp = path.join(path.dirname(__file__),"templates/formFile.html")
		html = template.render(temp,{'url':upload_url}) 
		self.response.out.write(html)
		
class UploadBlobstore(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		resources=''
		myfiles = self.get_uploads('file')  # 'file' is file upload field in the form
		self.redirect('/serveAll/')
		
class ServeBlobstore(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self,resource):
		resource = str(urllib.unquote(resource))
		blob_info = blobstore.BlobInfo.get(resource)
		self.send_blob(blob_info)

class ServeAll(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self):
		files = blobstore.BlobInfo.all()
		images=[]
		logging.info(images)
		for i in files:
			images.append('/serve/'+str(i.key()))
		temp = path.join(path.dirname(__file__),"templates/images.html")
		html = template.render(temp,{'images':images}) 
		logging.info(html)
		self.response.out.write(html)	
		
def main():
	application = webapp.WSGIApplication([
		('/blobstore/', Blobstore),
		('/upload/', UploadBlobstore),
		('/serve/(.*)', ServeBlobstore),
		('/serveAll/', ServeAll),
		('/.*', FormHandler),
		],
		debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

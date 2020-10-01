#!/usr/bin/python3

import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError
from PIL import Image
import argparse
import time
from html.parser import HTMLParser


pool = set()
images = []
total = 0
errors=0

def get_domain(link):
	x = urllib.parse.urlparse(link)
	#return tuple with (http//domain/path, domain)
	return (f"{x.scheme}://{x.netloc}{x.path}",x.netloc)

class html_parser(HTMLParser):
	def __init__(self):
		self.localfiles = set()
		HTMLParser.__init__(self)   

	def handle_starttag(self, tag, attrs):
		for a in attrs:
			if tag=="a" and "href" in a:
				if not a[1].startswith("https"):
					self.localfiles.add(urllib.parse.urljoin(link,a[1]))
				elif get_domain(link)[1] in link:
					self.localfiles.add(get_domain(link)[0])
			
			if tag=="img" and 'src' in a:
				#(src,' ') if src not ' '
				if a[1]:
					images.append(urllib.parse.urljoin(link, a[1]))	

					

def get_info(image):
	results = {}
	results[image] = {}
	with Image.open(urllib.request.urlopen(images)) as im:
		#JPEG IMAGEFILE
		results[images]["width"],results[images]["height"]= im.size
	return results

def crawler(url1, depth, maxdepth, total):
	#If url in pool or depth not reached
	global errors
	if url1 in pool or depth>=maxdepth or len(pool)>5:
		return None	
	else:
		pool.add(url1)
		html = html_parser()
		try:
			time.sleep(1)
			url = urllib.request.urlopen(url1)
			result = url.read().decode('utf-8')
			html.feed(str(result))
			total+=len(html.localfiles)
			print(f"Website: {url1} has {len(html.localfiles)}")
			
			for each in html.localfiles:
				#print(f"length:{len(html.localfiles)} and url:" + url1)
				#print("Going for " + str(depth)+ " " + str(len(html.localfiles)) + each)
				crawler(each,depth+1,maxdepth,total)


		except HTTPError as e:
			errors+=1
		
		except URLError as r:
			errors+=1


		print(len(html.localfiles))

	

	


if __name__=="__main__": 
	parser = argparse.ArgumentParser()
	parser.add_argument("--url", help="url to crawl")
	parser.add_argument("--depth", help="depth url visit", type=int)
	args = parser.parse_args()

	depth = 0
	link = args.url
	print(get_domain("https://github.com/features#team-management"))
	#crawler(url,depth,depthmax,total url visited)
	crawler(args.url,depth,args.depth,total)	
	for each in images:
		print(each)


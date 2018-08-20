## Import Section
from bs4 import BeautifulSoup
import requests
import re
import os
import jsmin

## Declaration Section
url = "" # URL to enter, example (http://www.google.com)

js_minify_link = "https://closure-compiler.appspot.com/compile"
css_minify_link = "https://cssminifier.com/raw"

# All RegEx Patterns
url_pattern = "^(http|https)://"
url_slash_pattern = "^//"
min_js_pattern = ".min.js$"
min_css_pattern = ".min.css$"

## Process Section
# Getting Source
result = requests.get(url)

# Parsing Source
soup = BeautifulSoup(result.content, 'html.parser')

# Getting JS Links
print "Getting JS Links"
scripts = soup.find_all('script') 

# Minifying each unminified JS Script
for script in scripts:
	src = script.get('src')
	if src:
		tempurl = ""
		if re.search(url_pattern, src):
			tempurl = ""
		elif re.search(url_slash_pattern, src):
			tempurl = "http:" 
		else:
			tempurl = url
		
		if not re.search(min_js_pattern, src):
			script_src = requests.get(tempurl + src)
			script_min_src = jsmin.jsmin(script_src.content)
			directory = os.path.dirname(src)
			if not os.path.exists(directory):
				os.makedirs(directory)
			with open(src, "w+") as file:
				file.write(script_min_src)
				print src + " minified Successfully"
		
print "JS minify Done"

# Getting CSS Stylesheets Links
print "Getting CSS Links"
links = soup.find_all("link")
# Minifying each unminified CSS Stylesheet.
for link in links:
	if link.get('rel')[0] == "stylesheet":
		href = link.get('href')
		if href:
			tempurl = ""
			if re.search(url_pattern, href):
				tempurl = ""
			elif re.search(url_slash_pattern, href):
				tempurl = "http:" 
			else:
				tempurl = url
			if not re.search(min_css_pattern, href):
				style_src = requests.get(tempurl + href)
				style_min_src = requests.post(css_minify_link, data = {
					'input': style_src.content
				}, verify=False)
				directory = os.path.dirname(href)
				if directory[0] == "/":
					directory = directory[1:]
					href = href[1:]
				if not os.path.exists(directory):
					os.makedirs(directory)
				with open(href, "w+") as file:
					file.write(style_min_src.content)
					print href + " minified Successfully"

print "CSS minify Done"

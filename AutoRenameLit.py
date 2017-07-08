# open and read data.xml

import re
import os
import shutil
errors = []
datafile = open("data.xml", "r", -1, "utf-8")
data = datafile.read()
print ("Copying PDFs...")
fdir = re.search(r'(path=")(.*?)(.enl)(\")', data).group(2) + ".Data\\PDF"
tdir = re.search(r"(.*\\)(.*)(\\)", fdir).group(1) + "PDFs"

try:
    os.stat(tdir)
except:
    os.mkdir(tdir)

for lit in re.finditer(r"(<record>)(.+?)(\/record>)", data):
	ref = lit.group(0)
	longtitle = re.search(r"(<title>)(.+?)(\>)(.+?)(\<)(.+?)(\/title>)", ref)
	if longtitle != None:
		longtitle = longtitle.group(4)
	else:
		continue
	shorttitle = re.search(r"(<secondary-title>)(.+?)(\>)(.+?)(\<)(.+?)(\/secondary-title>)", ref)
	if shorttitle != None:
		shorttitle = shorttitle.group(4)
	else:
		shorttitle = ""
	author = re.search(r"(<author>)(.+?)(\>)(.+?)(,)", ref)
	if author != None:
		author = author.group(4)
	else:
		author = ""
	year = re.search(r"(<year>)(.+?)(\>)(\d{4})", ref)
	if year != None:
		year = year.group(4)
	else:
		year = "0000"
	flocation = re.search(r"(internal-pdf:)(.*?)(<)", ref)
	if flocation != None:
		flocation = fdir + re.search(r"(internal-pdf:)(.*?)(<)", ref).group(2)[1:].replace("/", '\\')
	else:
		errors.append(longtitle+" has no attachment"+ "\n\n\n") 
		continue
	tlocation = re.search(r"(internal-pdf:)(.*?)(\d{10})(.*?)(<)", ref)
	if flocation != None:
		tlocation = tdir + re.sub(r'[^a-zA-Z0-9\- ]',r'',author) + year[2:] + "_" + re.sub(r'[^a-zA-Z0-9\- ]',r'',longtitle) + ".pdf"
	try:
		shutil.copy(flocation, tlocation)
	except OSError as why:
		errors.append(flocation,"\n", tlocation,"\n", str(why),"\n\n\n")
		print ("error: %s" % flocation)
		continue

print ("Done")
if errors:
 	print (errors)


import re
import os
import shutil
errors = []


# open and read data.xml. This file should be placed in the same folder of
# the python programm. The pdf files are save in 'PDFs' folder with the
# *.enl file.
datafile = open("data.xml", "r", -1, "utf-8")
data = datafile.read()

fdir = re.search(r'(path=")(.*?)(.enl)(\")', data).group(2) + ".Data\\PDF"
tdir = re.search(r"(.*\\)(.*)(\\)", fdir).group(1) + "PDFs"

# If the target directory is not there, then 'mkdir'
try:
    os.stat(tdir)
except AttributeError:
    os.mkdir(tdir)


# Start to copy files according to he xml file.
print ("Copying PDFs...")


for lit in re.finditer(r"(<record>)(.+?)(\/record>)", data):
    ref = lit.group(0)
    longtitle = re.search(r"(<title>)(.+?)(\>)(.+?)(\<)(.+?)(\/title>)", ref)
    # Find longtitle (normal title)
    if longtitle is not None:
        longtitle = longtitle.group(4)
    else:
        continue
    # Find short title (if possible)
    shorttitle = re.search(
        r"(<secondary-title>)(.+?)(\>)(.+?)(\<)(.+?)(\/secondary-title>)", ref)
    if shorttitle is not None:
        shorttitle = shorttitle.group(4)
    else:
        shorttitle = ""
    # Use short title if exist
    if len(shorttitle) > 5:
        title = shorttitle
    else:
        title = longtitle
    # Find Author (1st author's fam.name only)
    author = re.search(r"(<author>)(.+?)(\>)(.+?)(,)", ref)
    if author is not None:
        author = author.group(4)
    else:
        author = ""
    # Find Year in yyyy
    year = re.search(r"(<year>)(.+?)(\>)(\d{4})", ref)
    if year is not None:
        year = year.group(4)
    else:
        year = "0000"
    # Find PDF location
    flocation = re.search(r"(internal-pdf:)(.*?)(<)", ref)
    if flocation is not None:
        flocation = fdir + \
            re.search(r"(internal-pdf:)(.*?)(<)",
                      ref).group(2)[1:].replace("/", '\\')
    else:
        errors.append(longtitle + " has no attachment" + "\n\n\n")
        continue
    # Format target location and remove invalid char
    tlocation = re.search(r"(internal-pdf:)(.*?)(\d{10})(.*?)(<)", ref)
    if flocation is not None:
        tlocation = tdir + re.sub(r'[^a-zA-Z0-9\- ]', r'', author) + year[
            2:] + "_" + re.sub(r'[^a-zA-Z0-9\- ]', r'', longtitle) + ".pdf"
    # Copy the PDF to the target location
    try:
        shutil.copy(flocation, tlocation)
    except OSError as why:
        errors.append(flocation, "\n", tlocation, "\n", str(why), "\n\n\n")
        print ("error: %s" % flocation)
        continue

print ("Done")
if errors:
    print (errors)

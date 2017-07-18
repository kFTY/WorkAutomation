import urllib.request
import re
from bs4 import BeautifulSoup


# Produce the URLs
urlhead = "https://www.thorlabs.de/thorproduct.cfm?partnumber="
urls = []
partlist1 = []
qty = []
with open("partlist.txt", "r", -1, 'utf-8') as partlist:
    partnumber = partlist.read().splitlines()

for name in partnumber:
    name1 = re.search(r"(.*?)(\t)(.*)", name)
    if name1 is not None:
        qty.append(name1.group(3))
        name1 = name1.group(1)
        urls.append("%s%s" % (urlhead, name1))
        partlist1.append(name1)


# Download HTML file
i = 0
for url in urls:
    # remove signs in the file name
    namef = "".join(x for x in partlist1[i] if x.isalnum())
    try:
        urllib.request.urlretrieve(url, "/tmp/%s" % namef)
        print ("downloading", partlist1[i])
    except:
        print ("error")
    i += 1

# Find out the part name


def getNamePrice(partnumber):
    file = ""
    soupfile = ""
    # remove signs in the file name
    namef = "".join(x for x in partnumber if x.isalnum())
    try:
        file = open("/tmp/%s" % namef, "r", -1, 'utf-8')
    except:
        file = ""
        print ("cannot find")
        return ["", "", ""]

    soupfile = BeautifulSoup(file, "lxml")

    # wash the name string
    name = str(soupfile.title)
    name = name[18:-8]
    name = name[name.find(" ") + 1:]

    # wash the price string
    price = str(soupfile.find("font"))
    price = price[price.find(">") + 1:-9]
    price = price.replace(",", ".")

    return [name, partnumber, price]


# Get Name and Price for all parts
outputfile = open("output.txt", "w", -1, 'utf-8')
i = 0
for name in partlist1:
    print ("getting information for %s" % name)
    outputfile.write(getNamePrice("%s" % name)[0])
    outputfile.write("\t\t")
    outputfile.write(getNamePrice("%s" % name)[1])
    outputfile.write("\t")
    outputfile.write(getNamePrice("%s" % name)[2])
    outputfile.write("\t")
    outputfile.write(qty[i])
    outputfile.write("\n")
    i += 1

print ("Done")

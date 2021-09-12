import urllib.request

page = urllib.request.urlopen('http://textfiles.com/adventure/aencounter.txt')

content = page.read()
f.write(content)
f.close()

print(content)
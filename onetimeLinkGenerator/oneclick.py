import requests 
import time
import random

token_list = [line.strip() for line in open("token_file.txt", 'r')]
random.shuffle(token_list)





link_slug = [];
cnt = 1
for secret in token_list:
    r = requests.post('https://1ty.me/?mode=ajax&cmd=create_note', data = {'note':secret, 'email':'','reference':'', 'newsletter':''})
    response = r.json()
    link_slug.append(response['url'])
    print("done -",cnt)
    cnt += 1

linkstr = "https://1ty.me/"
links= []
for slug in link_slug:
    links.append(linkstr+slug)

print(links)

with open('generated_links.txt', 'w') as f:
    for item in links:
        f.write("%s\n" % item)
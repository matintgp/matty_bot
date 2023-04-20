import requests 
token = 'e8b4e8bc82027dfdea0e871ee91b90f9/'
URL = 'https://favqs.com/api/qotd'

response = requests.request('get',URL)
j = (response.json())['quote']
print(j)
date = (response.json())['qotd_date']
tags = j['tags']
url = j['url']
author = j['author']
quote = j['body']

l = len(tags)
tags = ''.join(tags)
tags = tags.replace(' ','#')

if l>0: 
    text = f'{quote}\n\nAuthor: {author}\ntag: #{tags}\n{url}'
    print(text)
else:
    text = f'{quote}\n\nAuthor: {author}\n{url}'
    print(text)

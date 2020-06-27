import requests
x=requests.get('http://127.0.0.1:20203',headers={'confirm':'fuckme'})
print(x)
print(x.text,type(x.text))
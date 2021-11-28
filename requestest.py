import requests


url = 'http://mtucitopteam.xyz/random/test'
answer = requests.get(url)
print(answer)
print(answer.json())
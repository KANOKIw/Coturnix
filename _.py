import requests

res = requests.post("https://kanokiw.com/short_my_url", { "url": "https://kanokiw.com/log" })
short_url = f"https://knkw.pw/u?{res.json()['shorted']}"
print(short_url)

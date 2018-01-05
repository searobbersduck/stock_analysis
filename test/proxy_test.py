import requests

url = "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000513.phtml?year=2007&jidu=3"

proxy = requests.get("http://127.0.0.1:5010/get/").text
proxy = "http://{}".format(proxy)

print(proxy)

req = requests.get(url=url, proxies={"http": proxy})
# req = requests.get(url=url)

print(req.text)
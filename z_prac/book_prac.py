import requests
from bs4 import BeautifulSoup

index = '028013'

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(f"http://book.interpark.com/display/collectlist.do?_method=BestsellerHourNew201605&bestTp=1&dispNo={index}",
    headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
book = soup.select('#content > div.rankBestWrapper > div.rankBestContainer > div.rankBestContents > div > div.rankBestContentList > ol > li')
# print(book)
for b in book:
    title = b.select_one('div > a > div.itemName > strong').text
    img = b.select_one('div > div.cover > div.coverImage > label > a > img')['src']
    url = b.select_one('div > div.cover > div.coverImage > label > a')['href']
    author = b.select_one('div > a > div.itemMeta > span.author').text
    print(title,img,f"http://book.interpark.com{url}",author)


    # dic = {'img': img, 'title': title, 'writer': writer, 'url': (f"http://book.interpark.com{url}")}
    # booklist.append(dic)
    # print(book.text)

# return jsonify({'booklist': booklist})

# 소설
# http://book.interpark.com/display/collectlist.do?_method=BestsellerHourNew201605&bestTp=1&dispNo=028005
# 역사
# http://book.interpark.com/display/collectlist.do?_method=BestsellerHourNew201605&bestTp=1&dispNo=028010
# 인문
# http://book.interpark.com/display/collectlist.do?_method=BestsellerHourNew201605&bestTp=1&dispNo=028013


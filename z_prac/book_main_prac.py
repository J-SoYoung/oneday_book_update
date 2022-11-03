import requests
from bs4 import BeautifulSoup

best_book = 'https://book.interpark.com/product/BookDisplay.do?_method=detail&sc.shopNo=0000400000&sc.prdNo=355136828&sc.saNo=003003001&bid1=Best_zone&bid2=LiveRanking&bid3=PRD&bid4=001'

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(best_book,headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
main_title = soup.select_one('#inc_titWrap > div.prod_title > div > h2').text
main_img = soup.select_one('#inc_optionWrap > div.optionLeft_wrap > div.bookBox > div > div > div > img')['src']
main_author = soup.select_one('#inc_optionWrap > div.optionRight_wrap > div.bookInfoBox > ul > li:nth-child(1) > a').text
main_text = soup.select_one('#bookInfoWrap > div:nth-child(4) > div > p').text.lstrip()
print(main_text)

    # dic = {'img': img, 'title': title, 'writer': writer, 'url': (f"http://book.interpark.com{url}")}
    # booklist.append(dic)
    # print(book.text)

# return jsonify({'booklist': booklist})

# jwt로그인, 회원가입, 서버 외, 파일저장, date 및 time 라이브러리
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename

from datetime import datetime, timedelta
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

# 크롤링 - beautifulsoup 임포트
import requests
from bs4 import BeautifulSoup

# DB사용
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.aphlzi8.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.miniPJ



##### html화면 렌더 API #####
@app.route('/')
# 메인 페이지 렌더
def home():
    # 로그인 성공후, 쿠키에 저장한 값을 가져온다.
    token_receive = request.cookies.get('mytoken')
    try:
        # 암호화를 푼다 (토큰+시크릿키+알고리즘) / user정보를 찾는다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        user = user_info['username']
        return render_template('index.html', user = user )
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
# 로그인 페이지 렌더
def login():
    return render_template('login.html')




##### 기능 API #####
@app.route('/main', methods=['GET'])
# book_list 보여주기
def booklist():
    # type에 따라 보여주는 booklist가 다름
    type_receive = request.args.get('type_give')

    # DB에 저장하지 않고 빈 배열 안에 크롤링 결과값을 넣음
    booklist = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(
        f"http://book.interpark.com/display/collectlist.do?_method=BestsellerHourNew201605&bestTp=1&dispNo={type_receive}",
        headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    book = soup.select(
        '#content > div.rankBestWrapper > div.rankBestContainer > div.rankBestContents > div > div.rankBestContentList > ol > li')

    for b in book:
        title = b.select_one('div > a > div.itemName > strong').text
        author = b.select_one('div > a > div.itemMeta > span.author').text
        img = b.select_one('div > div.cover > div.coverImage > label > a > img')['src']
        url = b.select_one('div > div.cover > div.coverImage > label > a')['href']
        # print(title,img,f"http://book.interpark.com{url}")

        doc = {
            'title': title,
            'author': author,
            'img': img,
            'url': f"http://book.interpark.com{url}",
        }
        # print(doc)

        # DB저장이 아닌 arrya에 넣음 append
        booklist.append(doc)

    return jsonify({'msg' : '리스트 가져오기성공', 'booklist':booklist})


@app.route('/mainBook', methods=['GET'])
# book_main 보여주기
def bookmain():

    bookmain = [];
    best_book = 'https://book.interpark.com/product/BookDisplay.do?_method=detail&sc.shopNo=0000400000&sc.prdNo=355136828&sc.saNo=003003001&bid1=Best_zone&bid2=LiveRanking&bid3=PRD&bid4=001'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(best_book, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    main_title = soup.select_one('#inc_titWrap > div.prod_title > div > h2').text
    main_img = soup.select_one('#inc_optionWrap > div.optionLeft_wrap > div.bookBox > div > div > div > img')['src']
    main_author = soup.select_one(
        '#inc_optionWrap > div.optionRight_wrap > div.bookInfoBox > ul > li:nth-child(1) > a').text
    main_text = soup.select_one('#bookInfoWrap > div:nth-child(4) > div > p').text.lstrip()

    doc = {
        'm_title': main_title,
        'm_author': main_author,
        'm_img': main_img,
        'm_text': main_text,
        'm_url': best_book,
    }
    # print(doc)

    # DB저장이 아닌 arrya에 넣음 append
    bookmain.append(doc)
    return jsonify({'msg' : '메인 가져오기성공', 'bookmain':bookmain})



@app.route('/sign_in', methods=['POST'])
# 로그인
def sign_in():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    print('로그인 유저 정보', username_receive)

    # 회원가입 때와 같은 방법으로 pw를 암호화한다. 암호화한 pw값으로 매칭되는 유저를 찾는다
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
            # 'exp': datetime.utcnow() + timedelta(seconds=5)  # 로그인 5초 test
        }
        # localhost:5000에서는 .decode('utf-8')삭제후 실행, 배포시 .decode('utf-8')를 포함
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        print('db저장 완료 :', payload['id'])
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/check_dup', methods=['POST'])
# ID 중복확인
def check_dup():
    username_receive = request.form['username_give']

    # id중복확인의 결과를 T(중복있음),F(없음)로 exists에 저장함
    exists = bool(db.users.find_one({"username": username_receive}))
    print(exists,'중복없음-사용가능')
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/sign_up/save', methods=['POST'])
# 회원가입
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
    }
    print(doc)
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
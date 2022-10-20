# python interpreter 
### 미니PJ를 위해 설치한 패키지들(간단하게 설명)
- flask : python서버 생성을 위함
- pyJWT : jwt를 이용한 로그인 기능을 위함
- bs4 : 웹스크래핑을 위함
- dnspython : pymongo연동을 위함
- pymongo : mongoDB atlas 사용
- requests : 서버와 API통신을 위함
<br>
![image](https://user-images.githubusercontent.com/85012454/196973993-2202cb36-6aea-495b-825e-b35d3d69fc0e.png)
<br>


# 회원가입- ID중복확인 ( sign_up / check_dup )<br>
#### 클라<br>
- ID, PW 입력 받기
- ID 빈칸 유무 확인 / 정규식에 맞는지 확인 -> 불합격 is-danger / 합격 is-loading
- 중복확인 -> 서버에 입력받은 ID넘겨주기<br>
#### 서버<br>
- DB에 ID있는지 확인 후 결과값을 T/F로 넘겨줌<br>
#### 클라 <br>
- ID중복 is-danger / ID사용가능 is-success , is-loading 삭제<br>
- is-danger, is-loading, is-success는 bulma css class명, css스타일링 및 상태관련 표시<br>
<br>

# 회원가입 - ID저장 ( sign_up / save )
#### 클라
- help-id의 클래스명을 확인한다 ( is-danger, is-success, is-loading )
- is-danger 있으면 아이디 확인 ( 빈칸이거나 정규식 통과 못한 ID )
- is-success 없으면 아이디 확인 ( 중복확인을 하지 않은 ID ), 있으면 비밀번호 검사로 넘어가기 
- 비밀번호 확인 : 빈칸, 정규식인지 확인
- 비밀번호, 비밀번호 확인이 같은지 확인 -> 서버에 입력받은 ID와 PW 넘겨주기
#### 서버
- PW는 암호화를 시킨다.
- 받아온 ID, 암호화 된PW, 앞으로 생성할 닉네임, 프로필 사진, 프로필 기본 사진, 자기소개  DB 저장
#### 클라
- 성공msg보내고 , 로그인 페이지로 이동
<br>

# 로그인 ( sign_in )
#### 클라
- ID/ PW입력받고 간단 검사 ( 빈칸 확인 ) -> 서버에 전달
#### 서버
- PW는 회원가입 때와 같은 방법으로 암호화를 시킨 후, ID와 함께 DB에서 매칭되는 유저를 찾는다
- 토큰(암호화 된 유저정보 + 만료기간)을 발행한다.
- 성공 메세지와 토큰을 보내준다
#### 클라
- 서버 결과가 유저를 찾았다면 토큰을 받아와 쿠키(key:value)에 저장한다.
- 메인페이지로 이동한다

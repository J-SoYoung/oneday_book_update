const titleDay = document.querySelector('.main_title .title_day')
const titleWeekend = document.querySelector('.main_title .title_weekend')
const clock = document.querySelector('.main_clock .clock')
const AMPM = document.querySelector('.main_clock .AMPM') 

// 메인 날짜
function today(){
  const date = new Date()
  const year = date.getFullYear()
  const month = date.getMonth()+1
  const day = date.getDate()
  titleDay.textContent = (`${month}월 ${day}일` )
}
today()

function weekend(){
  const date = new Date()
  const week = ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일']
  const weekDay = week[date.getDay()]
  titleWeekend.textContent = (weekDay)
}
weekend()


// 메인 시계
function timeAMPM(){
  const today = new Date().getHours
    if (today < 12){
      AMPM.textContent = 'am'
    } else {
      AMPM.textContent = 'pm'
    }  
}
timeAMPM()

function getTime(){
  const date = new Date()
  const hours = String(date.getHours()).padStart(2,'0')
  const minutes = String(date.getMinutes()).padStart(2,'0') 
  const second = String(date.getSeconds()).padStart(2,'0') 

  clock.textContent = (`${hours} : ${minutes} : ${second}`)
}
getTime()
setInterval(getTime, 1000)


// 메인 배경
const mainImg = document.querySelector('.main_bg')
const images = [ 
  'bg1.jpg', 'bg2.jpg', 'bg3.jpg', 'bg4.jpg', 
  'bg5.jpg', 'bg6.jpg', 'bg7.jpg', 'bg8.jpg' 
];
const randomImg = images[Math.floor(Math.random()*images.length)];
const bgImage = document.createElement("img");
bgImage.src = `../static/img/${randomImg}`;
mainImg.appendChild(bgImage)

// 로그인 창 활성버튼
function loginHandler() {
    $("#login").toggleClass("is-hidden")
}

// 로그인-회원가입BOX 분할
function toggle_sign_up() {
    //jquery를 사용해 toggle기능 추가, bulma-css의 is-hidden이 있으면 삭제, 없으면 추가
    $("#sign-up-box").toggleClass("is-hidden")
    $("#div-sign-in-or-up").toggleClass("is-hidden")
    $("#btn-check-dup").toggleClass("is-hidden")
    $("#help-id").toggleClass("is-hidden")
    $("#help-password").toggleClass("is-hidden")
    $("#help-password2").toggleClass("is-hidden")
}



// 로그인
function sign_in() {
    let username = $("#input-username").val()
    let password = $("#input-password").val()
    console.log(username, password)

    if (username == "") {
        $("#help-id-login").text("아이디를 입력해주세요.")
        $("#input-username").focus()
        return;
    } else {
        $("#help-id-login").text("")
    }

    if (password == "") {
        $("#help-password-login").text("비밀번호를 입력해주세요.")
        $("#input-password").focus()
        return;
    } else {
        $("#help-password-login").text("")
    }

    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            username_give: username,
            password_give: password
        },
        success: function (response) {
            alert(response['result'])
            if (response['result'] == 'success') {
                // 로그인이 되면, 토큰을 받아와 mytoken(key)으로 쿠키에 저장한다.
                // 토큰: 검증받은id + 유효시간, 쿠키: 브라우저의 database
                $.cookie('mytoken', response['token'], {path: '/'});

                // 메인페이지로 이동
                window.location.replace("/")
            } else {
                alert(response['msg'])
            }
        }
    });
}


// 중복확인
function check_dup() {
    let username = $("#input-username").val()
    console.log(username)

    // username이 빈칸인 경우 => class에 is-danger넣어주고, is-safe는 지운다
    // is- bulma css 스타일링임 safe, danger, loading, hidden
    if (username == "") {
        $("#help-id").text("아이디를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#input-username").focus()
        return;
    }

    // is_username = 정규식, 정규식에 만족하지 않는 경우 => class에 is-danger넣어주고, is-safe는 지운다
    if (!is_username(username)) {
        $("#help-id").text("아이디의 형식을 확인해주세요. 2-10자의 영문과 숫자만 입력 가능합니다.")
            .removeClass("is-safe").addClass("is-danger")
        $("#input-username").focus()
        return;
    }
    // 정규식 통과 후 서버에서 username 중복확인 / is-loading(bulma css 상태설정)
    $("#help-id").addClass("is-loading")

    $.ajax({
        type: "POST",
        url: "/sign_up/check_dup",
        data: {
            username_give: username
        },
        success: function (response) {
            if (response["exists"]) {
                $("#help-id").text("이미 존재하는 아이디입니다.").removeClass("is-safe").addClass("is-danger")
                $("#input-username").focus()
            } else {
                $("#help-id").text("사용할 수 있는 아이디입니다.").removeClass("is-danger").addClass("is-success")
            }
            $("#help-id").removeClass("is-loading")
        }
    });
}


// ID 정규표현식
function is_username(asValue) {
    var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$/;
    //2-10자의 영문과 숫자와 일부 특수문자(._-)만 입력 가능.
    return regExp.test(asValue);
}

// PW 정규표현식
function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    //영문과 숫자 조합의 8-20자. 특수문자(!@#$%^&*)입력 가능
    return regExp.test(asValue);
}

// 회원가입
function sign_up() {
    let username = $("#input-username").val()
    let password = $("#input-password").val()
    let password2 = $("#input-password2").val()
    console.log(username, password, password2)

    // help-id의 클래스명 확인
    if ($("#help-id").hasClass("is-danger")) {
        alert("아이디를 다시 확인해주세요.")
        return;
    } else if (!$("#help-id").hasClass("is-success")) {
        alert("아이디 중복확인을 해주세요.")
        return;
    }

    // 중복확인 통과됐으면 PW검사
    if (password == "") {
        // 비밀번호 빈칸확인
        $("#help-password").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#input-password").focus()
        return;
    } else if (!is_password(password)) {
        // 비밀번호 정규표현식 확인
        $("#help-password").text("비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자 사용가능 8-20자")
            .removeClass("is-safe").addClass("is-danger")
        $("#input-password").focus()
        return
    } else {
        // 비밀번호 정규식 통과
        $("#help-password").text("사용할 수 있는 비밀번호입니다.").removeClass("is-danger").addClass("is-success")
    }

    // 비밀번호1 - 비밀번호2 확인 같은지
    if (password2 == "") {
        $("#help-password2").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#input-password2").focus()
        return;
    } else if (password2 != password) {
        $("#help-password2").text("비밀번호가 일치하지 않습니다.").removeClass("is-safe").addClass("is-danger")
        $("#input-password2").focus()
        return;
    } else {
        $("#help-password2").text("비밀번호가 일치합니다.").removeClass("is-danger").addClass("is-success")
    }

    // PW-PW확인이 같으면 서버로 회원가입 정보전송
    $.ajax({
        type: "POST",
        url: "/sign_up/save",
        data: {
            username_give: username,
            password_give: password
        },
        success: function (response) {
            alert("회원가입을 축하드립니다!")
            window.location.replace("/login")
        }
    });

}
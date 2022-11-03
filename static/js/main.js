$(document).ready(function () {
    book_list_show('028013');
    book_main_show();
});

function book_list_show(type) {
    let bookType = type
    $('.list_book').empty()

    // 크롤링 해서 리스트 보여줌
    $.ajax({
        type: 'GET',
        url: `/main?type_give=${bookType}`,
        data: {},
        success: function (response) {
            let list = response['booklist']
            console.log(list)
            for (let i=0; i<list.length; i++){
                let title = list[i]['title']
                let img = list[i]['img']
                let url = list[i]['url']
                let author = list[i]['author']

                let temp_html = `
                <div class="list">
                    <a href="${url}" target="_blank">
                        <img class="list_img" src="${img}">
                        <p class="list_title">${title}</p>
                    </a>
                </div>`

                $('.list_book').append(temp_html)
            }
        }
    })
}

function book_main_show() {
    // 크롤링 해서 리스트 보여줌
    $.ajax({
        type: 'GET',
        url: '/mainBook',
        data: {},
        success: function (response) {
            let bookmain = response['bookmain'][0]
            console.log(bookmain)
            let m_title = bookmain['m_title']
            let m_img = bookmain['m_img']
            let m_text = bookmain['m_text']
            let m_author = bookmain['m_author']
            let m_url = bookmain['m_url']
            // console.log(m_title)
            let m_temp_html = `
                <div class="main_recommend">
                    <p class="main_title">오늘,<br>추천도서</p>
                    <a href="${m_url}" target="_blank" >자세히 보기</a>
                </div>
                <div class="today_img"><img src="${m_img}"></div>
                <div class="book_info">
                    <p class="name">${m_title}</p>
                    <p class="author">${m_author}</p>
                    <div class="text">줄거리
                        <p class="text_cont">${m_text}</p>
                    </div>
                </div>`
            $('.today_main').append(m_temp_html)

        }
    })
}


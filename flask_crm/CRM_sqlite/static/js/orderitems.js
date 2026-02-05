const current_path = window.location.pathname;
const search_field = document.getElementById('search_field');
const input_query = document.getElementById('input_query');
const submit = document.getElementById('submit');
const orderby = document.getElementById('orderby');

// nav바에서 페이지 버튼 활성화 -> 페이지 로드할 때마다 확인하여 적용
let section = current_path.split('/')[1];
const links = document.querySelectorAll('.nav_link');
links.forEach(link => {
    const link_section = link.getAttribute('data-section')
    if (link_section === section){
        link.classList.add('active')
    }
})

// 검색어 유지
const params = new URLSearchParams(window.location.search)
if (params.get('id')){
    search_field.value = 'id'
    input_query.value = params.get('id')
}
if (params.get('order_id')){
    search_field.value = 'order_id'
    input_query.value = params.get('order_id')
}
if (params.get('store_id')){
    search_field.value = 'store_id'
    input_query.value = params.get('store_id')
}
if (params.get('orderby')){
    orderby.value = params.get('orderby')
}

// 검색 조건 폼 제출 
submit.addEventListener('click', (e)=>{
    input_query.name = search_field.value
})
// 검색 내용 초기화
reset.addEventListener('click', (e)=>{
    search_field.value = ''
    input_query.value = ''
    store_type.value = ''
})


// 정렬 이벤트 리스너 
orderby.addEventListener('change', (e)=>{
    const query = new URL(window.location);
    query.searchParams.set('orderby', e.target.value)
    query.searchParams.set('page', 1)
    window.location.href = query
})

// 페이지 이동 버튼 이벤트 리스너
const start_btn = document.getElementById('start_page')
const prev10 = document.getElementById('prev10')
const prev = document.getElementById('previous')
const pages = document.getElementById('pagination')
const next = document.getElementById('next')
const next10 = document.getElementById('next10')
const end_btn = document.getElementById('end_page')

start_btn.addEventListener('click', ()=>{
    change_page(1)
})
end_btn.addEventListener('click', ()=>{
    console.log('마지막 페이지 버튼 누름')
    fetch_orderitems_data()
        .then(data =>{
            const end = data.end_page
            change_page(end)
        })
})
prev.addEventListener('click', ()=>{
    const current_page = get_current_page()
    change_page(current_page - 1)
})
prev10.addEventListener('click', ()=>{
    const current_page = get_current_page()
    change_page(current_page - 10)
})
next.addEventListener('click', ()=>{
    const current_page = get_current_page()
    change_page(current_page + 1)
})
next10.addEventListener('click', ()=>{
    const current_page = get_current_page()
    fetch_orderitems_data()
        .then(data =>{
            const end = data.end_page
            if ((current_page + 10)> end){
                change_page(end)
            } else {
                change_page(current_page + 10)
            }
        })
})

// 페이지버튼 부모요소에 이벤트 리스너 등록하기
pages.addEventListener('click', function(e){
    console.log('페이지 버튼에 이벤트 리스너 실행')
    // 페이지 버튼 요소 각각에 클릭 이벤트 등록하기
    if (e.target.tagName == 'BUTTON'){
        console.log(e.target.textContent)
        const page = e.target.textContent
        change_page(Number(page))
    }
})

window.onpopstate = function(e) {
    const page = e.state?.page || get_current_page()
    change_page(page, false) // false는 url을 다시 pusthState로 기록하지 않기 위함.
}

// 현재 페이지 가져오는 함수
function get_current_page() {
    const params = new URLSearchParams(window.location.search)
    console.log('--------현재 페이지 가져오는 함수 실행: ', params)
    let current_page = params.get('page')
    console.log('현재 페이지는? ', current_page)
    if (!current_page || isNaN(current_page) || current_page < 1){ // current_page가 빈값(Null)이거나 숫자가 아닌 경우(isNaN)
        current_page = 1
        const url = new URL(window.location);
        url.searchParams.set('page', current_page);
        history.pushState({page: current_page}, '', url);
        console.log('현재 페이지 없으면 1 ', current_page)
        return Number(current_page)
    }
    return Number(current_page)
}
// 주문아이템 정보 한 행에 입력하는 함수
function render_orderitem(orderitem) {
    const ths = ['id','order_id','item_id']
    const new_tr = document.createElement('tr')
    for (let key of ths) {
        const new_td = document.createElement('td')
        switch (key) {
            case 'id':
                new_td.innerText = orderitem[key]
                new_tr.appendChild(new_td)
                break
            case 'order_id':
                const new_as = document.createElement('a')
                new_as.href = `/orders/info/${orderitem[key]}`
                new_as.innerText = orderitem[key]
                new_td.appendChild(new_as)
                new_tr.appendChild(new_td)
                break
            case 'item_id':
                const new_au = document.createElement('a')
                new_au.href = `/items/info/${orderitem[key]}`
                new_au.innerText = orderitem[key]
                new_td.appendChild(new_au)
                new_tr.appendChild(new_td)
                break
        }
    }
    return new_tr
}
// 주문아이템 목록 렌더링하는 함수
function render_orderitems(orderitems) {
    console.log('-----render_orderitems 함수 실행')
    console.log('주문아이템 데이터 수: ', orderitems.length)
    const orderitem_list = document.getElementById('tbody')
    const search_result = document.getElementById('search_result')
    orderitem_list.innerHTML = ''
    search_result.textContent = ''
    if (orderitems.length == 0) {
        search_result.textContent = "검색 조건에 해당하는 주문아이템을 찾을 수 없습니다."
    } else {
        for (u of orderitems) {
            const new_tr = render_orderitem(u)
            orderitem_list.appendChild(new_tr)
        }
    }
}

// 페이지 버튼 렌더링하는 함수
function render_page_btns(end) {
    console.log('-----render_page_btns 함수 실행')
    current_page = get_current_page() 
    // 페이지 버튼 비활성화 여부
    if (current_page == end) {
        next.disabled = true;
        end_btn.disabled = true;
    } else {
        next.disabled = false;
        end_btn.disabled = false;
    }
    if (current_page == 1){
        start_btn.disabled =true;
        prev.disabled = true;
    } else {
        start_btn.disabled = false;
        prev.disabled = false;
    }
    if (current_page <= 10){
        prev10.disabled = true;
    } else {
        prev10.disabled = false;
    }
    if (Math.floor((current_page-1)/10) == Math.floor((end-1)/10)) {
        next10.disabled = true;
    } else {
        next10.disabled = false;
    }

    const btns_per_page = 10 // 한 페이지에 보여줄 페이지 버튼 수
    const first_page = Math.floor((current_page - 1) / btns_per_page )*btns_per_page + 1
    const tenth_page = Math.floor((current_page - 1) / btns_per_page)*btns_per_page + btns_per_page
    const end_page_first = Math.floor((end - 1) / btns_per_page)*btns_per_page + 1
    pages.innerHTML = '' // 페이지 번호 초기화
    if (first_page === end_page_first) {
        for (let page = end_page_first; page <= end; page++) {
            const pagelink = document.createElement('button')
            pagelink.textContent = page
            pagelink.setAttribute('data-page', page)
            pages.appendChild(pagelink)
            if (page == current_page) {
                pagelink.classList.add('active')
            }
        }
    } else {
        for (let page = first_page; page <= tenth_page; page++) {
            const pagelink = document.createElement('button')
            pagelink.textContent = page
            pagelink.setAttribute('data-page', page)
            pages.appendChild(pagelink)
            if (page == current_page) {
                pagelink.classList.add('active')
            }
        }
    }
}

function fetch_orderitems_data() {
    console.log('-----fetch 함수 실행됨')
    const params = new URLSearchParams(window.location.search)
    const current_page = params.get('page')
    const id = params.get('id')
    const order_id = params.get('order_id')
    const item_id = params.get('item_id')
    const orderby = params.get('orderby')

    const query = new URLSearchParams()
    if (id) {query.set('id', id)}
    if (order_id) {query.set('order_id', order_id)}
    if (item_id) {query.set('item_id', item_id)}
    if (current_page) {query.set('page', current_page)}
    if (orderby) {query.set('orderby', orderby)}
    console.log('쿼리 내용: ', query)

    return fetch(`/api/orderitems/?${query.toString()}`) // blueprint 사용시 fetch경로
        .then(response => {
            if (response.status == 404) {
                window.location.href = '/404'
            }
            if (!response.ok){
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json()})
        .catch(error => {
            console.error('주문아이템 데이터 로딩 중 오류: ', error);
            return {orderitems: [], end_page: 0}
        })
}

function render_page(data) {   
        console.log('-----render_page 실행')
        const orderitems  = data.orderitems
        const end_pages = data.end_page
        // 사용자 목록 렌더링
        render_orderitems(orderitems)
        // 페이지 번호 렌더링
        render_page_btns(end_pages)
}

function change_page(page, pushState=true) {
    console.log('-----페이지 로드')
    // url 변경(history.pushState 사용)
    if (pushState) {
        const url = new URL(window.location);
        url.searchParams.set('page', page);
        history.pushState({page: page}, '', url);
        }
    fetch_orderitems_data()
    .then(data => {
        render_page(data)
    })
}

change_page(1, false)
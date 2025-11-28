const current_path = window.location.pathname;
const update = document.getElementById('update')
const delete_ = document.getElementById('delete')
const store_id = document.getElementById('store_id')
const store_type = document.getElementById('store_type')
const store_name = document.getElementById('store_name')
const address = document.getElementById('address')
const store = document.getElementById('store')
const tbody = document.getElementById('tbody')
const monthly_sales = document.getElementById('monthly_sales')
const most_visited = document.getElementById('most_visited')

// nav바에서 페이지 버튼 활성화 -> 페이지 로드할 때마다 확인하여 적용
let section = current_path.split('/')[1];
const links = document.querySelectorAll('.nav_link');
links.forEach(link => {
    const link_section = link.getAttribute('data-section')
    if (link_section === section){
        link.classList.add('active')
    }
})

const url = window.location.pathname
const last = url.split('/')
const storeid = last[last.length - 1] 

update.addEventListener('click', () => {
    fetch(`/api/v1/stores/update_store/${store_id.textContent}`, {
        method: 'put',
        headers: {'content-type': 'application/json'},
        body: JSON.stringify({
            id: store_id.textContent,
            name: store_name.value,
            type: store_type.value,
            address: address.value
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            render_store_in_input(data)
            alert('스토어 정보가 수정되었습니다.')
    })})

delete_.addEventListener('click', () => {
    fetch(`/api/v1/stores/delete_store/${store_id.textContent}`, {
        method: 'delete'
        })
        .then(response => response.json())
        .then(data =>{
            console.log(data.message)
            alert(data.message);
            window.location.href = '/stores';
        }
        )
    })

function load_store_type(store_types) {
    const store_type = document.getElementById('store_type')
    for (type of store_types) {
        const opt = document.createElement('option')
        opt.value = type
        opt.textContent = type
        store_type.appendChild(opt)
    }
}
function render_store_in_input(store) {
    store_id.textContent = store.id
    store_type.value = store.type
    store_name.value = store.name
    address.value = store.address
}

// 테이블 한 행에 정보 입력하는 함수
function render_table_row(ths, data) {
    const new_tr = document.createElement('tr')
    for (let key of ths) {
        const new_td = document.createElement('td')
        if (key == 'user_id'){
            const new_a = document.createElement('a')
            new_a.href = `/user/info/${data[key]}`
            new_a.innerText = data[key]
            new_td.appendChild(new_a)
            new_tr.appendChild(new_td)
        } else {
            new_td.innerText = data[key]
            new_tr.appendChild(new_td)
        }
    }
    return new_tr
    }

// fetch로 쿼리 정보 받아오기
fetch(`/api/v1/store_info/${storeid}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        load_store_type(data.store_types)
        render_store_in_input(data.store)
    }
)
// 스토어의 월간 매출액 받아오기
fetch(`/api/v1/store/monthly_sales/${storeid}`)
    .then(response => response.json())
    .then(data => {
        console.log('주문내역: ',data)
        if (data.length == 0){
            document.getElementById('search_monthly_sales').innerText = `월간 매출액이 없습니다.`
        } else {
            for (u of data) {
                const ths = ['monthly', 'revenue', 'cnt']
                const new_tr = render_table_row(ths, u)
                monthly_sales.appendChild(new_tr)
                }
            }
    })

fetch(`/api/v1/store/most_visited/${storeid}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.length == 0){
            document.getElementById('search_most_visited').innerText = `단골 고객이 없습니다.`
        } else {
            for (i of data) {
                console.log(i)
                const ths = ['user_id', 'name', 'cnt']
                const new_tr = render_table_row(ths, i)
                most_visited.appendChild(new_tr)
            }
        }
    }
    )



const current_path = window.location.pathname;
const update = document.getElementById('update')
const delete_ = document.getElementById('delete')
const item_id = document.getElementById('item_id')
const item_name = document.getElementById('item_name')
const item_type = document.getElementById('item_type')
const price = document.getElementById('price')
const item = document.getElementById('item')
const tbody = document.getElementById('tbody')

// nav바에서 페이지 버튼 활성화 -> 페이지 로드할 때마다 확인하여 적용
let section = current_path.split('/')[1];
const links = document.querySelectorAll('.nav_link');
links.forEach(link => {
    const link_section = link.getAttribute('data-section')
    if (link_section === section){
        link.classList.add('active')
    }
})

// url에서 id 가져오기
const url = window.location.pathname
const last = url.split('/')
const itemid = last[last.length - 1] 

update.addEventListener('click', () => {
    console.log({
            id: item_id.textContent,
            type: item_type.value,
            name: item_name.value,
            price: price.value
        })
    fetch(`/api/v1/items/update_item/${item_id.textContent}`, {
        method: 'put',
        headers: {'content-type': 'application/json'},
        body: JSON.stringify({
            id: item_id.textContent,
            item_type: item_type.value,
            name: item_name.value,
            price: price.value,
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            render_item_in_input(data)
            alert('아이템 정보가 수정되었습니다.')
    })})

delete_.addEventListener('click', () => {
    fetch(`/api/v1/items/delete_item/${item_id.textContent}`, {
        method: 'delete'
        })
        .then(response => response.json())
        .then(data =>{
            console.log(data.message)
            alert(data.message);
            window.location.href = '/items';
        }
        )
    })

function load_item_type(item_types) {
    const item_type = document.getElementById('item_type')
    for (type of item_types) {
        const opt = document.createElement('option')
        opt.value = type
        opt.textContent = type
        item_type.appendChild(opt)
    }
}

function render_item_in_input(item) {
    item_id.textContent = item.id
    item_type.value = item.type
    item_name.value = item.name
    price.value = item.price
}
// 테이블 한 행에 정보 입력하는 함수
function render_table_row(ths, data) {
    const new_tr = document.createElement('tr')
    for (let key of ths) {
        const new_td = document.createElement('td')
        new_td.innerText = data[key]
        new_tr.appendChild(new_td)
    }
    return new_tr
    }

// fetch로 쿼리 정보 받아오기
fetch(`/api/v1/item_info/${itemid}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        load_item_type(data.item_types)
        render_item_in_input(data.item)
    }
)

// 최근 1년간 월간 매출액 정보 받아오기
fetch(`/api/v1/items/monthly_sales/${itemid}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.length == 0) {
            document.getElementById('search_monthly_sales').innerText = '최근 월간 매출액 정보가 없습니다.'
        }
        const ths = ['month', 'revenue', 'cnt']
        let month = []
        let revenue = []
        let count = []
        for (i of data) {
            console.log(i)
            const new_tr = render_table_row(ths, i)
            document.getElementById('item_sales').appendChild(new_tr)
            month.push(i.month)
            revenue.push(i.revenue)
            count.push(i.cnt)
        }
        month.reverse()
        revenue.reverse()
        count.reverse()
        // 차트그리기
        const ctx = document.getElementById('chart')
        const sales_data = {
            labels: month,
            datasets:[{
                type: 'line',
                label: '월별 매출액',
                data: revenue,
                yAxisID: 'y'
            }, {
                type: 'bar',
                label: '월별 판매개수',
                data: count,
                yAxisID: 'y1'
            }]
        }
        const config = {
            type: 'scatter',
            data: sales_data,
            options: {
                scales: {
                    y: {
                        position: 'left',
                        beginAtZero: true,
                    },
                    y1: {
                        position: 'right',
                        beginAtZero: true,
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }}
        new Chart(ctx, config)
    })


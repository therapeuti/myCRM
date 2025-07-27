const order_id = document.getElementById('order_id')
const ordertime = document.getElementById('ordertime')
const order = document.getElementById('order')
const tbody = document.getElementById('tbody')
const orderitems = document.getElementById('orderitems')

const url2 = window.location.href
const url = window.location.pathname
const last = url.split('/')
const orderid = last[last.length - 1] 



function render_table_with_link(ths, data) {
    const new_tr = document.createElement('tr')
    for (let key of ths) {
        console.log(data)
        console.log(key)
        console.log(data[key])
        const new_td = document.createElement('td')
        switch (key) {
            case 'item_id':
                const new_a = document.createElement('a')
                new_a.href = `/items/info/${data[key]}`
                new_a.innerText = data[key]
                new_td.appendChild(new_a)
                new_tr.appendChild(new_td)
                break
            case 'store_id':
                const new_as = document.createElement('a')
                new_as.href = `/stores/info/${data[key]}`
                new_as.innerText = data[key]
                new_td.appendChild(new_as)
                new_tr.appendChild(new_td)
                break
            case 'user_id':
                const new_au = document.createElement('a')
                new_au.href = `/users/info/${data[key]}`
                new_au.innerText = data[key]
                new_td.appendChild(new_au)
                new_tr.appendChild(new_td)
                break
            default:
                new_td.innerText = data[key]
                new_tr.appendChild(new_td)
        }
    }
    return new_tr
}

// fetch로 주문 정보(스토어, 사용자 정보) 받아오기
fetch(`/api/order_info/${orderid}`)
    .then(response => response.json())
    .then(data => {
        console.log('주문 기본 정보 받아옴: ', data)
        order_id.innerText = `Order ID : ${data.order_id}`
        ordertime.innerText = `Order Time : ${data.ordertime}`
        const ths = ['store_id', 'store', 'user_id', 'user']
        const new_tr = render_table_with_link(ths, data)
        tbody.appendChild(new_tr)

    }
)
// 주문내역 받아오기
fetch(`/api/orders/items/${orderid}`)
    .then(response => response.json())
    .then(data => {
        console.log('주문내역: ',data)
        if (data.length == 0){
            document.getElementById('search_orderitmes').innerText = `주문내역이 없습니다.`
        } else {
            for (u of data) {
                console.log(u)
                const ths = ['item_id', 'item', 'price']
                const new_tr = render_table_with_link(ths, u)
                orderitems.appendChild(new_tr)
                }
            }
    })

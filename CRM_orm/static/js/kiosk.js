const store_type = document.getElementById('store_type')
const store_name = document.getElementById('store_name')
const items = document.getElementById('items')
const add_order = document.getElementById('order')

// url에서 사용자 아이디 가져오기
const url = window.location.pathname
const last = url.split('/')
const user_id = last[last.length - 1] 
console.log(user_id)

store_type.addEventListener('change', (e) => {
    store_name.style.display = "inline-block";
    console.log(e.target.value)
    fetch(`/api/store_name/${e.target.value}`)
        .then(response => response.json())
        .then(data => {
            store_name.options.length = 0
            const default_opt = document.createElement('option')
            default_opt.innerText = '매장을 선택하세요.'
            store_name.add(default_opt)
            console.log(data)
            for (i of data) {
                console.log(i.name)
                const new_opt = document.createElement('option')
                new_opt.value = i.id
                new_opt.innerText = i.name
                store_name.appendChild(new_opt)
            }
        })
    })

store_name.addEventListener('change', (e) => {
    // document.getElementById('store_for_order').innerText = store_name.options[store_name.selectedIndex].text
    const store_id = e.target.value
    console.log(store_id)
    fetch('/api/items')
        .then(response => response.json())
        .then(data => {
            items
            for (i of data) {
                console.log(i)
                const new_tr = document.createElement('tr')
                new_tr.innerHTML = `<td>${i.type}</td>
                                    <td class="item">${i.name}</td>
                                    <td class="unit_price">${i.price}</td>
                                    <td>
                                        <button type="button" class="subst">-</button>
                                        <input class="number" type="number" value=0 min=0 max=50 data-id=${i.id}>
                                        <button type="button" class="plus">+</button>
                                    </td>
                                    <td class="price"></td>`       
                items.appendChild(new_tr)
                
            }
            
        })
    })

document.addEventListener('click', (e) => {
    if (e.target.classList.contains('subst')) {
        e.preventDefault()
        console.log(e.target);
        const input = e.target.parentElement.querySelector('.number')
        
        input.value = parseInt(input.value) - 1
        console.log(input.value)
        if (input.value < 0) {
            input.value = 0;
        }

        const tr = e.target.closest('tr')
        calculate_price(tr)
        // totalPrice(tr)
        sum_price()
    }
    if (e.target.classList.contains('plus')) {
        e.preventDefault();
        const input = e.target.parentElement.querySelector('.number')
        input.value = parseInt(input.value) + 1
        console.log(input.value)
        if (input.value > 50){
            alert('최대 수량은 50개를 넘을 수 없습니다.')
            input.value = 50

        }
        const tr = e.target.closest('tr')
        calculate_price(tr)
        // totalPrice(tr)
        sum_price()
    }    
    })

add_order.addEventListener('click', (e) => {
    console.log('주문 추가....')
    console.log('사용자 아이디: ', user_id)
    const store_id = store_name.value;
    console.log('스토어 아이디: ', store_id)
    const items = document.getElementById('items').rows
    const item_ids = []
    for (i = 1; i < items.length; i++) {
        console.log('for문 들어옴')
        console.log(items[i].cells[3].querySelector('.number').value)
        console.log(items[i].cells[3].querySelector('.number').dataset.id)
        const value = items[i].cells[3].querySelector('.number')
        if (value.value >= 1) {
            const id = items[i].cells[3].querySelector('.number').dataset.id
            item_ids.push(id)
        }
        value.value = 0
        items[i].cells[4].innerText = ''
        document.getElementById('total_price').innerText = ''
        e.target.disabled = true
    }
    console.log(item_ids)
    if (item_ids.length != 0) {
        const order_data = {
            'user_id': user_id,
            'store_id': store_id,
            'items': item_ids
        }
        fetch('/api/add_order', {
            method: 'POST',
            headers: {'content-type': 'application/json; charset=UTF-8'},
            body: JSON.stringify(order_data)                
        })
        .then(response => response.json()) 
        .then(data => {
            console.log(data)
        })
        alert('상품이 주문되었습니다!')
    } else {
        console.log('주문할 상품이 없음.')
        alert('주문할 상품이 없습니다. 상품을 선택해주세요!')
    }
})

function load_store_type(store_types) {
    const store_type = document.getElementById('store_type');
    store_type.innerHTML = '';
    const opt1 = document.createElement('option');
    opt1.innerText = '매장 종류를 선택하세요.';
    opt1.value = '';
    store_type.appendChild(opt1);
    for (type of store_types) {
        const opt1 = document.createElement('option');
        opt1.value = type;
        opt1.textContent = type;
        store_type.appendChild(opt1);
    }
}


function calculate_price(tr) {
    const unit_price = tr.querySelector('.unit_price').innerText
    console.log(unit_price)
    const number = tr.querySelector('.number').value
    console.log(number)
    const price = tr.querySelector('.price')
    price.innerText = parseInt(number) * parseInt(unit_price)
    console.log(tr.querySelector('.number').dataset.id)
    add_order.disabled = false
    
}

function totalPrice(tr) {
    console.log(tr)
    const orderlist = document.getElementById('order_list')
    const new_li = document.createElement('li')
    const item = tr.querySelector('.item').innerText
    const unit_price = tr.querySelector('.unit_price').innerText
    const number = tr.querySelector('.number').value
    const price = parseInt(unit_price) * parseInt(number)
    console.log(item)
    console.log(unit_price)
    console.log(number)
    console.log(price)
    new_li.innerText = `${item} x ${number} = ${price}`
    console.log(new_li)
    console.log(orderlist)
    orderlist.appendChild(new_li)
}

function sum_price() {
    const total_price = document.getElementById('total_price')
    const items = document.getElementById('items').rows
    let sum = 0
    for (i = 1; i < items.length; i++){
        const price = items[i].cells[4].innerText
        if (price) {
            console.log(price)
            sum += parseInt(price)
            console.log(sum)
        }
    }
    console.log(sum)
    total_price.innerText = `총 구매금액: ${sum}원`

}

fetch(`/api/user_info/${user_id}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('welcome').innerText = `어서오세요, ${data.name}님(${data.id})`
    })

fetch(`/api/store_type`)
    .then(response => response.json())
    .then(data => {
        load_store_type(data)
    }
    )
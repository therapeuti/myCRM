const current_path = window.location.pathname;
const update = document.getElementById('update')
const delete_ = document.getElementById('delete')
const user_id = document.getElementById('user_id')
const user_name = document.getElementById('user_name')
const birthdate = document.getElementById('birthdate')
const age = document.getElementById('age')
const gender = document.getElementById('gender')
const address = document.getElementById('address')
const user = document.getElementById('user')
const tbody = document.getElementById('tbody')
const store_top5 = document.getElementById('store_top5')
const item_top5 = document.getElementById('item_top5')

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
const userid = last[last.length - 1] 

update.addEventListener('click', () => {
    fetch(`/api/update_user/${user_id.textContent}`, {
        method: 'put',
        headers: {'content-type': 'application/json'},
        body: JSON.stringify({
            id: user_id.textContent,
            name: user_name.value,
            birthdate: birthdate.value,
            age: age.value,
            gender: gender.value,
            address: address.value
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            render_user_in_input(data)
            alert('사용자 정보가 수정되었습니다.')
    })})

delete_.addEventListener('click', () => {
    fetch(`/api/delete_user/${user_id.textContent}`, {
        method: 'delete'
        })
        .then(response => response.json())
        .then(data =>{
            console.log(data.message)
            alert(data.message);
            window.location.href = '/users';
        }
        )
    })


function render_user_in_input(user) {
    user_id.textContent = user.id
    user_name.value = user.name
    birthdate.value = user.birthdate
    age.value = user.age
    gender.value = user.gender
    address.value = user.address
}

// fetch로 쿼리 정보 받아오기
fetch(`/api/user_info/${userid}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        render_user_in_input(data)
    }
)
// 사용자의 주문내역 받아오기
fetch(`/api/order_history/${userid}`)
    .then(response => response.json())
    .then(data => {
        console.log('주문내역: ',data)
        if (data.length == 0){
            document.getElementById('p_order_history').innerText = `주문내역이 없습니다.`
        } else {
            for (u of data) {
                const new_tr = document.createElement('tr')
                new_tr.innerHTML = `<td><a href="/orders/info/${u.order_id}">${u.order_id}</td>
                    <td>${u.ordertime}</td>
                    <td>${u.store}</td>
                    <td>${u.item}</td>`
                    order_history.appendChild(new_tr)
                }
            }
    })

fetch(`/api/store_top5/${userid}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.length == 0){
            document.getElementById('p_store_top5').innerText = `주문내역이 없습니다.`
        } else {
            for (i of data) {
                const new_li = document.createElement('li')
                new_li.innerText = `${i.store} : ${i.cnt}번 방문`
                store_top5.appendChild(new_li)
            }
        }
    }
    )

fetch(`/api/item_top5/${userid}`)
    .then(response => response.json())
    .then(data => {
        if (data.length == 0){
            document.getElementById('p_item_top5').innerText = `주문내역이 없습니다.`
        } else {
            for (i of data) {
                const new_li = document.createElement('li')
                new_li.innerText = `${i.item} : ${i.cnt}번 구매` 
                item_top5.appendChild(new_li)                    
            }}
    })

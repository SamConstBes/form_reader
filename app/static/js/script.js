let rawResults;

if (window.location.pathname === '/products') {
    localStorage.removeItem("requestId");
    document.addEventListener("DOMContentLoaded", function() {
        let container = document.getElementById('results-container');
        rawResults = JSON.parse(container.dataset.results);
        localStorage.setItem("result",  JSON.stringify(rawResults));
        initResults(rawResults);
    });
}

// Record data
function initResults(data) {
    rawResults = data;
    // Здесь делаем всё, что хотели: рендер, расчеты и т.д.
    console.log('Работаем с данными:', Object.keys(rawResults).length);
}

// Get data from dynamic row, render table, save in local storage
async function getDynamicForm(event, params) {
    event.preventDefault();
    const content = JSON.parse(localStorage.getItem("result"));
    const count = Object.keys(content).length
    const form = document.getElementById(params); 
    
    // Создаем объект со всеми данными формы
    const data = new FormData(form);
    console.log(data);
    if (!validateForm(data)) {
        showNotification('Заполните все поля!');
        return
    };
    
    // Конвертируем в обычный объект
    const payload = Object.fromEntries(data.entries());
    content[count] = payload;
    delete payload.action_id;

    const rowData = await uploadFile(payload); // if file: upload file

    const tbody = document.querySelector('#dynamic tbody');
    const tr = document.createElement('tr');
    Object.entries(rowData).forEach(([key, value]) => {
        const td = document.createElement('td');
        const keyName = key.replace('_', '');
        td.innerHTML = `<input type="text" name="${keyName}_${count}" value="${value}">`
        tr.appendChild(td);
    });

    tbody.appendChild(tr);
    const td1 = document.createElement('td');
    td1.innerHTML = `<img src="${rowData.prodPhoto || ''}" style="width: 50px;">`;
    tr.appendChild(td1);
    showNotification('Данные добавлены');
    localStorage.setItem("result",  JSON.stringify(content));
}

// upload file from input type=file
async function uploadFile(payload) {
    const result = {};
    for (const [key, value] of Object.entries(payload)) {
        const isFile = key.toLowerCase().includes('photo') || key.toLowerCase().includes('file');
        
        if (isFile && value) { 
            const formData = new FormData();
            formData.append('userFile', value);

            try {
                const response = await fetch('/uploadFile', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`Ошибка сервера: ${response.status}`);
                }
                const res = await response.json();
                result[key] = res['success']; 

            } catch (err) {
                console.error(err);
                alert(`Ошибка загрузки ${key}: ` + err.message);
                return false; 
            }
        } else result[key] = value;
    }
    return result;
}

// Validate form for empty
function validateForm(data) {
  for (const [key, value] of data.entries()) {
    if (key === 'prod_Photo' || key === 'prodPhoto') {continue}
    if (!value.trim()) {
      console.log(`Пустое поле: ${key}`);
      return false; 
    }
  }
  return true;
}

//  Show modal window with different content
async function showModal(event, check) {
    event.preventDefault();
    const modal = document.querySelector('.commentModal')
    modal.style.display = 'block';
    switch (check){
        case 'products':
            modal.querySelector('.btn-block').style.display = 'none';
            modal.querySelector('#commentInput').style.display = 'none';
            modal.querySelector('#commentText').innerHTML = 'Listening at: http://0.0.0.0:5000 (70303)';
            break;
        case 'index':
            modal.querySelector('.btn-alone').style.display = 'none';
            modal.querySelector('#commentText').innerHTML = 'Введите комментария для отправки';
            break;
        default:
            break;
    }
}

// Close modal window
function closeModal() {
    document.getElementById("commentModal").style.display = "none";
}

// Submit/Send data to server
async function submitForm(event, action) {
    event.preventDefault();
    const form = document.querySelector(`#${action}`);
    const path = `/${action}`
    const formData = new FormData(form);
    const grouped = Object.fromEntries(formData.entries());
  
    const products = Object.keys(grouped)
        .filter(key => key.startsWith('prodName_')) // Берем только базу (имена товаров)
        .map(key => {
        const index = key.split('_')[1]; // Извлекаем индекс: "0", "1"...
        
        return {
            prodName: grouped[`prodName_${index}`],
            prodPrice: parseInt(grouped[`prodPrice_${index}`], 10) || 0,
            prodLink: grouped[`prodLink_${index}`] || '#',
            prodPhoto: grouped[`prodPhoto_${index}`] || '',
        };
        });

    try {
        const response = await fetch(path, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ action: action, data: products})
        });
        if (!response.ok) {
            throw new Error(`Ошибка сети: ${response.status}, ${response.statusText}`);
        }
        window.location.reload();
        // const result = await response.json();
        // console.log(result)
    } catch (error) {
        console.error('Ошибка:', error.message || error);
    }
};

// Func for view notification
function showNotification(msg) {
    const notification = document.getElementById('notification');
    if (notification) {
        notification.innerText = msg;
        notification.style.display = 'block';
        setTimeout(() => {
            document.querySelector('.notification')?.remove();
        }, 3000);
    }
}

function clearForm(e, id) {
    e.preventDefault(); 
    document.getElementById(id).reset();
    // delete result.data; 
}

setTimeout(() => {
    document.querySelector('.flash-message')?.remove();
}, 3000);

let currentPostId = null;
const backBtn = document.getElementById('backBtn');
if (backBtn !== null) {
    backBtn.addEventListener("click", function() {
        window.location.href = '/history';
    });
}

// // Проверяем, было ли перенаправление успешным
// const notification = document.getElementById('notification');

// // Проверяем наличие параметра status в URL
// const urlParams = new URLSearchParams(window.location.search);
// if (urlParams.has('status') && urlParams.get('status') === 'success') {
//     notification.style.display = 'block';
//             setTimeout(() => {
//                 notification.classList.remove('show'); // Запуск анимации исчезания
//             }, 5000); 
// }
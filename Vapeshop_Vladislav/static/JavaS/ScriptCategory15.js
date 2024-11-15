
const list = document.querySelectorAll('#List_line .line');
const uniqueItems = new Set();

list.forEach(item => {
    if (uniqueItems.has(item.textContent)) {
        item.style.display = 'none';
    } else {
        uniqueItems.add(item.textContent);
    }
});

function toggleMenu() {
    const menu = document.getElementById('menu');
    if (menu.style.display === 'none' || menu.style.display === '') {
        menu.style.display = 'block';
    } else {
        menu.style.display = 'none';
    }
}
function toggleSubmenu(event) {
    event.stopPropagation();
    const submenu = event.currentTarget.querySelector('.submenu');
    if (submenu.style.display === 'none' || submenu.style.display === '') {
        const submenuitem = document.querySelectorAll('.submenu-item');
        const uniqueItems = new Set();
        submenu.style.display = 'block';
        submenuitem.forEach(item => {
            if (uniqueItems.has(item.textContent)) {
                item.style.display = 'none';
            } else {
                uniqueItems.add(item.textContent);
            }
        });
    } else {
        submenu.style.display = 'none';
    }
}

document.querySelectorAll('.catalog').forEach(catalog => {
    if (!catalog.querySelector('.product')) {
        catalog.style.display = 'none'; // Скрываем родительский блок
    }
});

document.querySelectorAll('.category').forEach(category => {
    const catalog = category.querySelector('.catalog');
    if (catalog && window.getComputedStyle(catalog).display === 'none') {
        category.style.display = 'none'; // Скрываем родительский блок
    }
});

document.querySelectorAll('.number-input').forEach(container => {
    const quantityInput = container.querySelector('#valueInput');

    container.querySelector('.increment').addEventListener('click', function() {
        quantityInput.value = parseInt(quantityInput.value) + 1;
    });

    container.querySelector('.decrement').addEventListener('click', function() {
        if (parseInt(quantityInput.value) > 0) {
            quantityInput.value = parseInt(quantityInput.value) - 1;
        }
    });})
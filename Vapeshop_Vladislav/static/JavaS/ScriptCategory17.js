
const list = document.querySelectorAll('#List_line .line');
const uniqueItems = new Set();

list.forEach(item => {
    if (uniqueItems.has(item.textContent)) {
        item.style.display = 'none';
    } else {
        uniqueItems.add(item.textContent);
    }
});

document.getElementById('menuButton').addEventListener('click', function(event) {
    var menuPanel = document.getElementById('menuPanel');
    menuPanel.classList.toggle('hidden');
    event.stopPropagation();
});

var categoryButtons = document.getElementsByClassName('categoryButton');
for (var i = 0; i < categoryButtons.length; i++) {
    categoryButtons[i].addEventListener('click', function(event) {
        var subcategoryPanel = this.nextElementSibling;
        subcategoryPanel.classList.toggle('hidden');
        event.stopPropagation();
    });
}

document.addEventListener('click', function(event) {
    var menuPanel = document.getElementById('menuPanel');
    if (!menuPanel.contains(event.target)) {
        menuPanel.classList.add('hidden');
    }
});

var subcategoryPanels = document.getElementsByClassName('subcategoryPanel');
for (var i = 0; i < subcategoryPanels.length; i++) {
    var subcategoryPanel = subcategoryPanels[i];
    var subcategoryItems = subcategoryPanel.getElementsByTagName('li');
    var seen = {};
    for (var j = 0; j < subcategoryItems.length; j++) {
        var item = subcategoryItems[j];
        var text = item.innerText;
        if (seen[text]) {
            item.style.display = 'none';
        } else {
            seen[text] = true;
        }
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
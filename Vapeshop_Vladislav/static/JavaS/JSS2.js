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

var subcategoryButtons = document.getElementsByClassName('subcategoryButton');
for (var i = 0; i < categoryButtons.length; i++) {
    subcategoryButtons[i].addEventListener('click', function(event) {
        var sub_subcategoryPanel = this.nextElementSibling;
        sub_subcategoryPanel.classList.toggle('hidden');
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
    var subcategoryItems2 = subcategoryPanel.getElementsByClassName('subcategoryButton');
    var subcategoryItems3 = subcategoryItems + subcategoryItems2
    var seen = {};
    for (var j = 0; j < subcategoryItems3.length; j++) {
        var item = subcategoryItems3[j];
        var text = item.innerText;
        if (seen[text]) {
            item.style.display = 'none';
        } else {
            seen[text] = true;
        }
    }
}

var sub_subcategoryPanels = document.getElementsByClassName('sub-subcategoryPanel');
for (var i = 0; i < sub_subcategoryPanels.length; i++) {
    var sub_subcategoryPanel = sub_subcategoryPanels[i];
    var sub_subcategoryItems = sub_subcategoryPanel.getElementsByTagName('li');
    var sub_seen = {};
    for (var j = 0; j < sub_subcategoryItems.length; j++) {
        var sub_item = sub_subcategoryItems[j];
        var sub_text = sub_item.innerText;
        if (sub_seen[text]) {
            sub_item.style.display = 'none';
        } else {
            sub_seen[text] = true;
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
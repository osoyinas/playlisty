const burger = document.getElementById('burger');
const menu = document.querySelector('.menu');

burger.addEventListener('change', (event) => {
    if (event.target.checked) {
        menu.classList.add('menu-visible');
    } else {
        menu.classList.remove('menu-visible');
    }
});
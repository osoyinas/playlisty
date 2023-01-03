const burger = document.getElementById('burger');
const menu = document.querySelector('.menu');
const loggedIn = document.querySelector('.log_text').textContent != "Log in with Spotify!"

burger.addEventListener('change', (event) => {
    if (event.target.checked) {
        menu.classList.add('menu-visible');
    } else {
        console.log("CACA")
        menu.classList.remove('menu-visible');
    }
});
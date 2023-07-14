const buttons = document.querySelectorAll('button')

buttons.forEach((button) => {
    console.log(button);

    button.addEventListener('click', () => {
        const url = button.getAttribute('url-data')
        window.location.href = url
    })
})

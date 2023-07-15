const buttons = document.querySelectorAll('button')

buttons.forEach((button) => {

    button.addEventListener('click', (e) => {
        e.preventDefault()
        const url = button.getAttribute('data-url')
        window.location.href = url
    })

})

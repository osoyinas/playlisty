const buttons = document.querySelectorAll('.fancy-button')
const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value

buttons.forEach((button) => {

    button.addEventListener('click', (e) => {
        e.preventDefault()
        const url = button.getAttribute('data-url')
        window.location.href = url
    })

})

const feedbackButton = document.getElementById('feedback-button')

feedbackButton.addEventListener('click', () => {
    console.log("Clicked");
    const scoreElement = document.getElementById('score')
    const descElement = document.getElementById('description')
    const score = scoreElement.value
    const desc = descElement.value
    fetch('/feedback/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,

        },
        body: JSON.stringify({ 'score': score, 'description': desc })
    })
        .then(
            response => response.json()
        )
        .then(data => {
        })
})
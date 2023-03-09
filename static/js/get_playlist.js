const nameInput = document.getElementById("name_input");
const submitButton = document.querySelector("submit_button");
const csrftoken = getCookie('csrftoken');

var idsList = []
var data = { name: "", list: [] }
var url = "/getplaylist/"

submitButton.addEventListener('click', (event) => {
    data.name = nameInput.value; 
    console.log("Clicked");
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(jsonData=>{
            window.location.href = jsonData.url;
        })
        .catch(error => {
            console.error('Error:', error);
        });
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
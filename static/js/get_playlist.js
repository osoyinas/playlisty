const nameInput = document.getElementById("name_input");
const submitButton = document.querySelector(".submit_button");
const csrftoken = getCookie('csrftoken');
const loader = document.querySelector(".loader");
const section = document.getElementById("create_playlist");
var idsList = []
var data = { name: "", list: [] }
var url = "/getplaylist/"


submitButton.addEventListener("click", async function () {
    let loggedIn = await checkLoggedIn();
    let notNamed = nameInput.value == "";
    if (!loggedIn) {
        alert('Login with Spotify!')
        return;
    }
    else if (notNamed) {
        alert('Name your playlist.');
        return;
    }

    else if (!checkSelectedArtists()){
        alert('Select artists!');
        return;
    }
    data.name = nameInput.value;
    loadingView();
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
        .then(
            response => response.json())
        .then(jsonData => {
            window.location.href = jsonData.url;
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
function checkSelectedArtists() {
    return data.list.length != 0;
}
function loadingView() {
    section.classList.add('hide');
    loader.classList.add('show');
}


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

async function checkLoggedIn() {
    let url = "/getloginstatus/";
    let loggedIn = false;
    try{
        const response = await fetch(url);
        const data = await response.json();
        loggedIn = data.status;
    }
    catch{
        loggedIn = false;
    }
    return loggedIn;
}
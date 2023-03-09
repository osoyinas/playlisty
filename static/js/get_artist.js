const searchInput = document.getElementById('search');
const searchWrapper = document.querySelector('.wrapper');
const resultsWrapper = document.querySelector('.results');
const submitForm = document.getElementById('playlist_form')
const bottomContainer = document.querySelector('.bottom');
const loggedIn = document.querySelector('.log_text').textContent != "Log in with Spotify!";
const emptyContainer = document.getElementById('empty');
const nameInput = document.getElementById("name_input");
var idsList = []
data = { name: "", list: [] }
const listArtists = async (str) => {
    try {
        if (str.length == 0) {
            searchWrapper.classList.remove('show');
            return;
        }
        else if (!loggedIn) {
            alert("Log in with Spotify!")
        }
        else {
            searchWrapper.classList.add('show');
            const response = await fetch(`./getartists/${str}`);
            const data = await response.json();
            if (data.message == "Success") {
                content = ``;
                data.artists.forEach(artist => {
                    content += `<li><button onclick="optionClicked(event)" class="option" value="${artist.id}">${artist.name}</button></li>`
                });
                resultsWrapper.innerHTML = `<ul>${content}</ul>`
            }
        }
    } catch (error) {
        console.log(error);
    }
};

function optionClicked(event) {
    artist_id = event.target.value;
    artist_name = event.target.textContent;
    searchInput.value = ``;
    resultsWrapper.innerHTML = ``;
    searchWrapper.classList.remove('show');
    if (data.list.includes(artist_id)) {
        return;
    }
    data.list.push(artist_id);
    bottomContainer.innerHTML += `<iframe as="style" style="border-radius:12px" src="https://open.spotify.com/embed/artist/${artist_id}" width="100%" height="80" frameBorder="0" allow="encrypted-media"></iframe>`;
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

const csrftoken = getCookie('csrftoken');

submitForm.addEventListener('submit', (event) => {
    event.preventDefault();
    data.name = nameInput.value;
    let url = "/generateplaylist/"
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
            // Redirect to the requested page
            console.log(jsonData);
            window.location.href = jsonData.url;
        })
        .catch(error => {
            console.error('Error:', error);
        });
})


const waitInit = async () => {
    searchInput.addEventListener('keyup', (event) => {
        let input = searchInput.value;
        listArtists(input);
    })
};

window.addEventListener("load", async () => {
    await waitInit();
});
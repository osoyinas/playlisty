const searchInput = document.getElementById('search-input');
const searchWrapper = document.querySelector('.wrapper');
const resultsWrapper = document.querySelector('.results');
const bottomContainer = document.querySelector('.bottom');
const emptyContainer = document.getElementById('empty');


function addArtist(artistId) {
    bottomContainer.innerHTML += `<iframe as="style" style="border-radius:12px" src="https://open.spotify.com/embed/artist/${artistId}" width="100%" height="80" frameBorder="0" allow="encrypted-media"></iframe>`;
}


function removeArtist(artistId) {
    return;
}

async function listArtists (str) {
    try {
        let loggedIn = await checkLoggedIn();
        if (str.length == 0) {
            searchWrapper.classList.remove('show');
            searchInput.value = ``;
            return;
        }
        else if (!loggedIn) {
            searchInput.value = ``;
            alert("Log in with Spotify!")
        }
        else {
            searchWrapper.classList.add('show');
            const response = await fetch(`./createplaylist/getartists/${str}`);
            const data = await response.json();
            if (data.message == "Success") {
                content = ``;
                data.artists.forEach(artist => {
                    content += artistResult(artist.id, artist.name)
                });
                resultsWrapper.innerHTML = `<ul>${content}</ul>`
            }
        }
    } catch (error) {
        console.log(error);
    }
}

function artistResult(artistId, artistName){
    return `<li><button onclick="optionClicked(event)" class="option" value="${artistId}">${artistName}</button></li>`
}


function optionClicked (event) {
    artistId = event.target.value;
    artistName = event.target.textContent;
    searchInput.value = ``;
    resultsWrapper.innerHTML = ``;
    searchWrapper.classList.remove('show');
    if (data.list.includes(artistId)) {
        return;
    }
    data.list.push(artistId); //save the artist id 
    addArtist(artistId);
}


async function  waitInit() {
    //every time the user types a letter, searchs for coincidence
    searchInput.addEventListener('keyup', (event) => {
        let input = searchInput.value;
        listArtists(input);
    })
}


window.addEventListener("load", async () => {
    await waitInit();
});
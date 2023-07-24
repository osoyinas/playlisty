//DOM ELEMENTS
const searchInput = document.getElementById("search-input")
const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value
const resultsWrapper = document.querySelector('.results-container ul')
const resultsContainer = document.querySelector('.results-container')
const generatePlaylistButton = document.getElementById("generate-playlist-button")
const playlistContainer = document.querySelector('.playlist-container')
const selectMenu = document.getElementById("select-menu")
const typeToSearchDisplay = document.querySelector('.display-results')
const emptyPlaylist = document.querySelector('.empty-playlists')
const domArtistsNumber = document.getElementById('artists-n')
const domAlbumsNumber = document.getElementById('albums-n')
const domTracksNumber = document.getElementById('tracks-n')
const domTotalNumber = document.getElementById('total-n')

var items_ids = []
var count = 0; //playlist items count
var timer = null //timer to delay the requests
var artistsNumber = 0
var albumsNumber = 0
var tracksNumber = 0

//User typed in search input
searchInput.addEventListener('input', () => startTimerAndFetch());


// Count 500ms and if the user hasnt typed again, fetch. If not, it restarts the timer
function startTimerAndFetch() {
    resultsContainer.classList.remove('show');
    typeToSearchDisplay.classList.add('hide');
    clearTimeout(timer) //reset timer
    timer = setTimeout(fetchData, 500);
}

async function fetchData() {
    resultsWrapper.innerHTML = `` //reset results
    let str = searchInput.value.trim()
    if (str == "") {
        return;
    }
    const response = await fetch(`./getitem/${str}/${getCurrentType()}`); //peticion GET
    const data = await response.json();
    if (data.status == "success") {
        updateResults(data)
    }
    else if (data.status == "error") {
        if (data.reason == "Not whitelisted") window.location.href = "/ups"
        else if (data.reason == "Not logged in") {
            console.log("HOLA");
        }
    }
    else {
        window.location.href = "/"
    }
}
function updateResults(data) {
    if (data.results.length == 0) {
        resultsWrapper.innerHTML += `<h2 class="">Not found</h2>`//no results 
        document.querySelector('#create-playlist h2').classList.add('show');
        resultsContainer.classList.add('show');
        return;
    }
    resultsWrapper.innerHTML = `` //reset results
    data.results.forEach((result) => {
        addToResultsItems(result)
    });
    document.querySelectorAll('.results-container ul li').
        forEach(function (item) { //Option clicked
            item.addEventListener('click', () => {
                resultsContainer.classList.remove('show');
                searchInput.value = ``
                addItemToPlaylistContainer(item.textContent, item.getAttribute('id-value'), item.getAttribute('type-value'), item.querySelector('img').getAttribute('src'), item.getAttribute('data-url'));
                setTimeout(() => {
                    resultsWrapper.innerHTML = ``
                }, 500);
            });
        });
    setTimeout(() => {
        resultsContainer.classList.add('show');
    }, 100);
}

//Add to the DOM the fetched items results.
function addToResultsItems(result) {
    //track doesnt contain images
    console.log(result);
    image = result.images.length > 0 ? result.images[0].url : 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fpluspng.com%2Fimg-png%2Fpng-user-icon-circled-user-icon-2240.png&f=1&nofb=1&ipt=44566a639661e2c0be63851cdfe96a5bbef2cc246fd13f817b67e1e1c6214592&ipo=images'
    resultsWrapper.innerHTML +=
        `<li id-value="${result.id}" type-value="${result.type}" data-url="${result.external_urls.spotify}">
        <img src="${image}" alt="${result.name}">
        ${result.name}
    </li>`
}
//Adds an item to the playlist container with its own options depending on the item
function addItemToPlaylistContainer(name, id, type, image, url) {
    let emptyPlaylist = document.querySelector('.empty-playlists')
    emptyPlaylist.classList.add('hide')
    if (items_ids.includes(id)) {
        return;
    }
    items_ids.push(id)
    count += 1;
    var newLi = document.createElement('li');
    newLi.setAttribute("id-value", id);
    newLi.setAttribute("type-value", type);
    newLi.setAttribute("data-url", url);
    let content =
        `
        <div class="left">
            <img src="${image}" alt="">
            <div class="name-type-container">
                <a  href= "${url}" target='_blank' rel= 'noreferrer noopener' class="name">${name}</a>
                <p class="type">${type}</p>
            </div>  
        </div>
        `
    switch (type) {
        case "artist":
            artistsNumber += 1
            domArtistsNumber.textContent = artistsNumber
            content +=
                `<div class="right">
                    <select name="options">
                        <option value="top-tracks" selected>top 10</option>
                        <option value="all-tracks">all</option>
                    </select>`;
            break;

        case "track":
            tracksNumber += 1
            domTracksNumber.textContent = tracksNumber
            content +=
                `<div class="right">
                    <select name="options">
                        <option value="just-this" selected>just this</option>
                        <option value="similar-tracks">similar tracks</option>
                    </select>`;
            break;

        case "album":
            albumsNumber += 1
            domAlbumsNumber.textContent = albumsNumber
            content +=
                `
                <div class="right">
                <select name="options">
                    <option value="all-tracks" selected>all tracks</option>
                </select>`;
            break;
    }

    content += `
                    <button class="button" onclick="deleteElement(this)">
                    <svg viewBox="0 0 448 512" class="svgIcon"><path d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"></path></svg>
                </button>
               
                </div>
                `
    newLi.insertAdjacentHTML('beforeend', content);
    domTotalNumber.textContent = albumsNumber + tracksNumber + artistsNumber
    setTimeout(() => {
        playlistContainer.appendChild(newLi);
        var item = document.querySelector('.playlist-container li[id-value="' + id + '"]');
        setTimeout(() => { item.classList.add('show'); }, 100)
    }, 400)
}


//Generate playlist button clicked, 
generatePlaylistButton.addEventListener('click', (e) => {
    e.preventDefault();
    if (items_ids.length == 0) {
        alert("Add items to your playlist!");
        return;
    }
    let selectedItems = { name: "", items: [] }
    let playlistItems = document.querySelectorAll('.playlist-container li');
    playlistItems.forEach((item) => {

        let object = {
            id: item.getAttribute('id-value'),
            type: item.getAttribute('type-value'),
            option: item.querySelector('select').value
        }
        selectedItems.name += item.querySelector(".name").textContent.trim() + ", "
        selectedItems.items.push(object)
    });
    console.log(selectedItems)
    let queryString = encodeURIComponent(JSON.stringify(selectedItems))
    window.location.href = '/createplaylist/?data=' + queryString
});

function getCurrentType() {
    return selectMenu.value;
}

selectMenu.addEventListener('change', function (event) {
    startTimerAndFetch();
});

function deleteElement(button) {
    // Obtén el elemento <li> que contiene el botón
    var listItem = button.closest("li");
    items_ids.pop(listItem.getAttribute('id-value'))
    // Elimina el elemento <li> de la lista
    listItem.classList.remove('show')
    type = listItem.getAttribute('type-value')
    switch (type) {
        case ('artist'):
            artistsNumber--
            domArtistsNumber.textContent = artistsNumber
            break
        case ('album'):
            albumsNumber--
            domAlbumsNumber.textContent = albumsNumber
            break
        case ('track'):
            tracksNumber--
            domTracksNumber.textContent = tracksNumber
            break
    }
    domTotalNumber.textContent = artistsNumber + albumsNumber + tracksNumber
    setTimeout(() => {
        listItem.remove();
        if (items_ids.length == 0) {
            let emptyPlaylist = document.querySelector('.empty-playlists')
            emptyPlaylist.classList.remove('hide')
        }
    }, 400);

}

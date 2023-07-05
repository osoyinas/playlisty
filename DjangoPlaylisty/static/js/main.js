//DOM ELEMENTS
const searchInput = document.getElementById("search-input")
const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value
const resultsWrapper = document.querySelector('.results-container ul')
const resultsContainer = document.querySelector('.results-container')
const generatePlaylistButton = document.getElementById("generate-playlist-button")
const playlistContainer = document.querySelector('.playlist-container')
const selectMenu = document.getElementById("select-menu")
const typeToSearchDisplay = document.querySelector('.display-results')
const emptyPlaylist = document.querySelector('.playlist-empty')
var items_ids = []  
var count = 0; //playlist items count
var timer = null //timer to delay the requests

//User typed in search input
searchInput.addEventListener('input', function (event) {
    startTimerAndFetch();
});


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
        else if (data.reason == "Not logged in") window.location.href = "/"
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
        addResultToDom(result)
    });
    document.querySelectorAll('.results-container ul li').
        forEach(function (item) {
            item.addEventListener('click', () => {
                resultsContainer.classList.remove('show');
                searchInput.value = ``
                addItemToPlaylistContainer(item.textContent, item.getAttribute('id-value'), item.getAttribute('type-value'), item.querySelector('img').getAttribute('src'));
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
function addResultToDom(result) {
    //track doesnt contain images
    image = result.images[0].url
    resultsWrapper.innerHTML +=
        `<li id-value="${result.id}" type-value="${result.type}">
        <img src="${image}" alt="${result.name}">
        ${result.name}
    </li>`
}

//Adds an item to the playlist container with its own options depending on the item
function addItemToPlaylistContainer(name, id, type, image) {
    emptyPlaylist.classList.add('hide')
    if (items_ids.includes(id)){
        return;
    }
    items_ids.push(id)
    count += 1;
    let content =
        `<li id-value="${id}" type-value="${type}">
            <div class="left">
                <img src="${image}" alt="">
                    <div class="name-type-container">
                        <p class="name">${name}</p>
                        <p class="type">${type}</p>
                    </div>  
            </div>
    `
    switch (type) {
        case "artist":
            content +=
                `<div class="right">
              <select name="options">
                <option value="top-tracks">top 10</option>
                <option value="all-tracks">all</option>
              </select>`;
            break;

        case "track":
            content +=
                `<div class="right">
              <select name="options">
                <option value="just-this">just this</option>
                <option value="similar-tracks">similar tracks</option>
              </select>`;
            break;

        case "album":
            content +=
                `<div class="right">
              <select name="options">
                <option value="all-tracks">all tracks</option>
              </select>`;
            break;
    }


    content += `
                    <button class="button" onclick="deleteElement(this)">
                    <svg viewBox="0 0 448 512" class="svgIcon"><path d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"></path></svg>
                </button>
            <img class = "right-icon" src="/static/svg/spotify_logo.png" alt="">    
                </div>
                </li>
                `
    playlistContainer.innerHTML += content;
    var item = document.querySelector('.playlist-container li[id-value="' + id + '"]');
    setTimeout(() => {
        item.classList.add('show')
    }, 400);

}


//Generate playlist button clicked, 
generatePlaylistButton.addEventListener('click', (e) => {
    e.preventDefault();
    if (items_ids.length == 0){
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
        selectedItems.items.push(object);
    });
    selectedItems.name = selectedItems.name.slice(0, 80).slice(0, -1) + "..."
    let url = "/getplaylist/"
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify(selectedItems)
    })
        .then(
            response => response.json()
        ).then(data => {
            if (data.message == "failed") {
                console.log("Error ocurred");
                return;
            }
            window.location.href = data.url
        })
        .catch(error => {
            console.error('Error:', error);
        });
    selectedItems.items = []
    selectedItems.name = ""
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
    setTimeout(() => {
        listItem.remove();
        if (items_ids.length == 0){
            emptyPlaylist.classList.remove('hide')
        }
    }, 400);

}

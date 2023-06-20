const searchInput = document.getElementById("search-input");
var timer = null
const resultWrapper = document.querySelector('.results-container ul');
resultsContainer = document.querySelector('.results-container');
const selectedItems = [];
const notFound = document.querySelector('#create-playlist h2')

searchInput.addEventListener('input', function (event) {
    startTimer()
});

function startTimer() {
    resultsContainer.classList.remove('show');
    clearTimeout(timer) //reset timer

    timer = setTimeout(fetchData, 200);
}

async function fetchData() {
    resultWrapper.innerHTML = `` //reset results
    let str = searchInput.value
    if (str == "") {
        return;
    }
    const response = await fetch(`./createplaylist/getartists/${str}`); //peticion GET
    const data = await response.json();
    if (data.status == "success") {
        updateResults(data)
    }
}

function updateResults(data) {
    if (data.results.length == 0) {
        resultWrapper.innerHTML+=`<h2 class="">Not found</h2>`//no results 
        document.querySelector('#create-playlist h2').classList.add('show');
        resultsContainer.classList.add('show');
        return;
    }
    resultWrapper.innerHTML = `` //reset results
    data.results.forEach((result) => {
        addResultToDom(result)
    });
    document.querySelectorAll('.results-container ul li').
    forEach(function (item) {
        item.addEventListener('click', ()=>{
            resultsContainer.classList.remove('show');
            searchInput.value = ``
            selectedItems.push(item.getAttribute('id-value'))
        });
    });
    setTimeout(() => {
        resultsContainer.classList.add('show');
    }, 100);
}

function addResultToDom(result) {
    let image = result.images.length > 0 ? result.images[0].url : "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Spotify_logo_without_text.svg/168px-Spotify_logo_without_text.svg.png"
    resultWrapper.innerHTML +=
        `<li id-value="${result.id}">
        ${result.name}
        <img src="${image}" alt="${result.name}">
    </li>`
}
//    <img src="${result.images[0].url}" alt="${result.name}">
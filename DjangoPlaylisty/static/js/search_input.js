const searchInput = document.getElementById("search-input");
var timer = null
const resultWrapper = document.querySelector('.results-container ul');
resultsContainer = document.querySelector('.results-container');
const selectedItems = [];


searchInput.addEventListener('input', function (event) {
    startTimer()
});

function startTimer() {
    resultsContainer.classList.remove('show');
    clearTimeout(timer) //reset timer

    timer = setTimeout(fetchData, 500);
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
        alert('sin resultados')
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
            console.log(selectedItems);
        });
    });
    setTimeout(() => {
        resultsContainer.classList.add('show');
    }, 100);
}

function addResultToDom(result) {
    resultWrapper.innerHTML +=
        `<li id-value="${result.id}">
        ${result.name}
    <img src="${result.images[0].url}" alt="${result.name}">
    </li>`
}

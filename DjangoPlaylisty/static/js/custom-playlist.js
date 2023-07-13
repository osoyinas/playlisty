const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value
const playlistItems = document.querySelectorAll('.playlist-container li')
const createPlaylistButton = document.getElementById('generate-playlist-button')
const nameInputValue = document.getElementById('name-input')

var items_ids = []

playlistItems.forEach((item) => {
    items_ids.push(item.getAttribute('id-value'));
})

function deleteElement(button) {
    // Obtén el elemento <li> que contiene el botón
    var listItem = button.closest("li");
    items_ids.pop(listItem.getAttribute('id-value'))
    // Elimina el elemento <li> de la lista
    listItem.classList.remove('show')
    setTimeout(() => {
        listItem.remove();
        if (items_ids.length == 0) {
            emptyPlaylist.classList.remove('hide')
        }
    }, 400);
    if (items_ids.length == 0) {
        alert("Emty playlist")
        window.location.href = "/"
    }
}

createPlaylistButton.addEventListener('click', (e) => {
    e.preventDefault();
    if (items_ids.length == 0) {
        alert("Add items to your playlist!");
        return;
    }
    let selectedItems = { name: nameInputValue.value, items: items_ids }
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
            let queryString = encodeURIComponent(JSON.stringify({url: data.url, id: data.id}))
            window.location.href = '/generatedplaylist/?data=' + queryString
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
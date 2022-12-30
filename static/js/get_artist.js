const searchInput = document.getElementById('search');
const searchWrapper = document.querySelector('.wrapper');
const resultsWrapper = document.querySelector('.results');
const hiddenInput = document.getElementById("list_ids")
const submitForm = document.getElementById('playlist_form')
const bottomContainer = document.querySelector('.bottom');
var list_id = []
const listArtists = async (str) => {
    try {
        if (str.length == 0) {
            searchWrapper.classList.remove('show');
            return;
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


const waitInit = async () => {
    searchInput.addEventListener('keyup', (event) => {
        let input = searchInput.value;
        listArtists(input);
    })
};

window.addEventListener("load", async () => {
    await waitInit();
});

function optionClicked(event) {
    artist_id = event.target.value;
    artist_name = event.target.textContent;
    searchInput.value = ``;
    resultsWrapper.innerHTML = ``;
    searchWrapper.classList.remove('show');
    if(list_id.includes(artist_id)){
        return;
    }
    list_id.push(artist_id);
    raw_string = ""
    list_id.forEach((id) => {
        raw_string += id + ","
    })
    bottomContainer.innerHTML += `<iframe as="style" style="border-radius:12px" src="https://open.spotify.com/embed/artist/${artist_id}" width="100%" height="80" frameBorder="0" allow="encrypted-media"></iframe> `
    hiddenInput.value = raw_string;
}
submitForm.addEventListener('submit',(event)=>{
    event.preventDefault();
    if (hiddenInput.value.length == 0){
        alert("Select artists");
    }    
    else{
        submitForm.submit();
    }
})
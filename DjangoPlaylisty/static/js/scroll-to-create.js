document.addEventListener("DOMContentLoaded", function() {
    const loader = document.querySelector('.loader')
    const section = document.querySelector('#create-playlist')
    loader.addEventListener("click", function() {
        section.scrollIntoView({ behavior: "smooth" });
    });
  });
  
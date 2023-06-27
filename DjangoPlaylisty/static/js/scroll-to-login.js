document.addEventListener("DOMContentLoaded", function() {
    const loader = document.querySelector('.loader')
    const section = document.querySelector('#login-to-start')
  
    loader.addEventListener("click", function() {
        section.scrollIntoView({ behavior: "smooth" });
    });
  });
  
console.log("SCROLL TO LOGIN");
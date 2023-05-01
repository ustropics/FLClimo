$(document).ready(function () {
  $("#sidebarCollapse").on("click", function () {
    $("#sidebar").toggleClass("active");
  });
});

// get all the links
const links = document.querySelectorAll('ul li a');

// get all the divs
const divs = document.querySelectorAll('.content-wrapper > div');

// add click event listeners to each link
for (let i = 0; i < links.length; i++) {
  const link = links[i];
  link.addEventListener('click', function(e) {
    e.preventDefault();
    // remove active class from specific links
    if (link.classList.contains('specific-link')) {
      for (let j = 0; j < divs.length; j++) {
        const div = divs[j];
        div.classList.remove('active');
      }
    }
    // add active class to the div that corresponds to the clicked link
    const id = link.getAttribute('id').replace('-link', '-wrapper');
    const divToShow = document.getElementById(id);
    console.log(id)
    divToShow.classList.add('active');
  });
}

// Get all navigation links
const navLinks = document.querySelectorAll('.nav-link');

// Add click event listener to each link
navLinks.forEach(link => {
  link.addEventListener('click', function() {
    // Remove "active" class from all links
    navLinks.forEach(link => {
      link.classList.remove('active');
    });
    // Add "active" class to clicked link
    this.classList.add('active');
  });
});
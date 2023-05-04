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

const navbarLinks = document.querySelectorAll('.navbar-link');
const sidebarLinks = document.querySelectorAll('.sidebar-link');
const sections = document.querySelectorAll('section');

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const sectionId = entry.target.getAttribute('id');
      const link = document.querySelector(`[href="#${sectionId}"]`);
      makeActive(link);
    }
  });
}, { threshold: 0.5 });

sections.forEach(section => {
  sectionObserver.observe(section);
});






// Define a function to activate a link in both menus
function activateLink(navSelector, sidebarSelector) {
  // Get the link in the navbar menu
  const navbarLink = document.querySelector(navSelector);

  // Get the link in the sidebar menu
  const sidebarLink = document.querySelector(sidebarSelector);

  // Add a click event listener to both links
  navbarLink.addEventListener('click', function(event) {
    event.preventDefault();

    // Remove the "active" class from any links that have it
    document.querySelectorAll('.nav-link').forEach(link => {
      link.classList.remove('active');
    });

    // Add the "active" class to the clicked link in both menus
    navbarLink.classList.add('active');
    sidebarLink.classList.add('active');
  });

  sidebarLink.addEventListener('click', function(event) {
    event.preventDefault();

    // Remove the "active" class from any links that have it
    document.querySelectorAll('.nav-link').forEach(link => {
      link.classList.remove('active');
    });

    // Add the "active" class to the clicked link in both menus
    navbarLink.classList.add('active');
    sidebarLink.classList.add('active');
  });
}

// Activate links in both menus
activateLink('.navbar-home-link', '#homepage-link');
activateLink('.navbar-features-link', '#features-link');


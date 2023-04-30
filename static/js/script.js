// Get references to DOM elements
const menu = document.querySelector('.menu');
const menuToggle = document.querySelector('.menu-toggle');
const buttons = document.querySelectorAll('.button');
const mainContent = document.querySelector('.main-content');

// Add event listener to toggle menu visibility on click of menu toggle button
menuToggle.addEventListener('click', () => {
  menu.classList.toggle('collapsed');
});

// Add event listeners to buttons to switch main content
buttons.forEach(button => {
  button.addEventListener('click', () => {
    // Remove the 'active' class from all buttons
    buttons.forEach(button => {
      button.classList.remove('active');
    });

    // Add the 'active' class to the clicked button
    button.classList.add('active');

    // Change the content based on the data-target attribute of the clicked button
    const target = button.getAttribute('data-target');
    mainContent.innerHTML = `<h2>${target}</h2><p>This is the ${target} content.</p>`;
  });
});

// Custom JavaScript for CacaoDocs

// Example: Add any custom interactivity or functionality here
document.addEventListener('DOMContentLoaded', function() {
  console.log('CacaoDocs custom JS loaded');
  
  // Example: Smooth scroll for sidebar links
  document.querySelectorAll('.ant-menu-item a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });
});
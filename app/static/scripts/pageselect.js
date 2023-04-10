// Get the current page's path
const currentPage = location.pathname;
// Get all the anchor elements within the header navigation
const links = document.querySelectorAll("header nav a");
// Iterate over each link element
links.forEach(function (link) {
  // If the link's pathname matches the current page's pathname,
  // add the "active" class to the link
  if (link.pathname === currentPage) {
    link.classList.add("active");
  }
});

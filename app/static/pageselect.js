var currentPage = location.pathname;
var links = document.querySelectorAll("header nav a");
links.forEach(function (link) {
  if (link.pathname === currentPage) {
    link.classList.add("active");
  }
});

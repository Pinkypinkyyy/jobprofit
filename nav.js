(function () {
  var nav = document.getElementById("pinkNav");
  var btn = document.getElementById("pinkBurger");
  if (!nav || !btn) return;
  btn.addEventListener("click", function () {
    nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", nav.classList.contains("open") ? "true" : "false");
  });
})();

document.addEventListener("DOMContentLoaded", (event) => {
  const start_menu = document.createElement("div");
  const hr = document.createElement("hr");
  const start_button = document.querySelector("span:last-of-type");

  start_menu.classList.add("start_menu");
  start_menu.appendChild(document.getElementsByTagName("H2")[0]);
  start_menu.appendChild(hr);
  start_menu.appendChild(document.getElementsByTagName("H3")[0]);
  start_menu.appendChild(document.getElementsByTagName("figure")[0]);

  document.body.appendChild(start_menu);

  document.addEventListener("click", (e) => {
    if (e.target === start_button) {
      start_menu.classList.toggle("visible");
    }

    if (start_menu.classList.contains("visible") && e.target !== start_button) {
      start_menu.classList.remove("visible");
    }
  });
});

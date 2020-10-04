document.addEventListener("DOMContentLoaded", (event) => {
  const sounds_folder = document.createElement("div");
  const sounds_folder_title = document.createElement("div");
  const sounds_icon = document.querySelector("span:first-of-type");
  const close_button = document.createElement("button");
  const sounds = document.querySelector("ul");
  const friends = document.getElementsByTagName("table")[0];
  sounds_folder.classList.add("sounds_folder");
  sounds_folder_title.classList.add("folder_title");
  sounds_folder_title.appendChild(close_button);
  sounds_folder.appendChild(sounds_folder_title);
  document.body.appendChild(sounds_folder);
  sounds_folder.append(sounds);
  sounds_icon.addEventListener("click", () => {
    sounds_folder.classList.toggle("visible");
  });
  close_button.addEventListener("click", () => {
    sounds_folder.classList.toggle("visible");
  });
  document.body.insertBefore(friends, sounds_icon);
});

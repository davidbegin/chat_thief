document.addEventListener("DOMContentLoaded", () => {
  let idle_time = 0;
  const idle_interval = setInterval(() => {
    idle_time++;
    if (idle_time >= 5 && !div_wrapper.classList.contains("visible")) {
      div_wrapper.classList.add("visible");
    }
  }, 1000);
  const div_wrapper = document.createElement("div");
  div_wrapper.classList.add("screensaver");
  document.body.appendChild(div_wrapper);
  this.document.addEventListener("mousemove", (e) => {
    idle_time = 0;
    div_wrapper.classList.remove("visible");
  });
  this.document.addEventListener("keypress", (e) => {
    idle_time = 0;
    div_wrapper.classList.remove("visible");
  });
});

window.addEventListener("load", function(){
    for (i=0;i<=10;i++) {
    d = document.createElement("div");
    d.className = "bubble x" + i;
    document.body.appendChild(d);
  }
});

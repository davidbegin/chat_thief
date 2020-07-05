function rgba() {
  var o = Math.round,
    r = Math.random,
    s = 255;
  return (
    "rgba(" + o(r() * s) + "," + o(r() * s) + "," + o(r() * s) + "," + 0.4 + ")"
  );
}
var divs = document.getElementsByTagName("a");
for (var i = 0; i < divs.length; i++) {
  var color = rgba();
  divs[i].style.boxSizing = "border-box";
  divs[i].style.border = "2pxsolid" + color;
  divs[i].style.backgroundColor = color;
}
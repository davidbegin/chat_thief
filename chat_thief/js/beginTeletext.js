window.onload = addDiv;
function addDiv(){
var links = document.getElementsByTagName("li");
for (var i=0; i<links.length; i++){
  links[i].innerHTML += ". . . " + i;
  links[i].setAttribute("id", "page"+i);
}
var newDiv = document.createElement('div');
newDiv.setAttribute("id", "pageNo");
var newContent = document.createTextNode("P100");
newDiv.append(newContent);
var currentDiv = document.getElementsByTagName("h1")[0];
document.body.insertBefore(newDiv, currentDiv);
}
document.addEventListener('keydown', function(e) {checkKeys(e);}); 
function checkKeys(event) {
  if(document.getElementById("pageNo").innerHTML.length >= 4){document.getElementById("pageNo").innerHTML = "P";}
  document.getElementById("pageNo").innerHTML = document.getElementById("pageNo").innerHTML + event.key;
  if(document.getElementById("pageNo").innerHTML.length >= 4){checkForPage(document.getElementById("pageNo").innerHTML);}
}
function checkForPage(page){
  var pageId = 'page'+page.slice(1);
  var linkOnly = document.getElementById(pageId).innerHTML.split('"');
  window.location.replace(linkOnly[1]);
}
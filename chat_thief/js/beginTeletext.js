window.addEventListener("load", function() {
var links = document.getElementsByTagName("li");
for (var i=0; i<links.length; i++){
  links[i].innerHTML += ". . . " + (parseInt(i)+101);
  links[i].setAttribute("id", "page"+ (parseInt(i)+101));
}
var newDiv = document.createElement('div');
newDiv.setAttribute("id", "pageNo");
var newContent = document.createTextNode("P100");
newDiv.append(newContent);
var currentDiv = document.getElementsByTagName("h1")[0];
document.body.insertBefore(newDiv, currentDiv);
});                  
document.addEventListener('keydown', function(e){if(e['key']>=0 && e['key']<=9){checkKeys(e);}});
function checkKeys(event) {
  if(document.getElementById("pageNo").innerHTML.length >= 4){document.getElementById("pageNo").innerHTML = "P";}
  document.getElementById("pageNo").innerHTML = document.getElementById("pageNo").innerHTML + event.key;
  if(document.getElementById("pageNo").innerHTML.length >= 4){checkForPage(document.getElementById("pageNo").innerHTML);}
}
function checkForPage(page){
  var pageId = 'page'+page.slice(1);
  var linkOnly = document.getElementById(pageId).innerHTML.split('"');
  window.location.href = (linkOnly[1]);
}
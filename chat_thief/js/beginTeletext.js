window.onload = addDiv;

function addDiv(){
var newDiv = document.createElement('div');
newDiv.setAttribute("id", "pageNo");
var newContent = document.createTextNode("P100");
newDiv.append(newContent);
var currentDiv = document.getElementsByTagName("h1");
currentDiv = currentDiv[0];
document.body.insertBefore(newDiv, currentDiv);
}

document.addEventListener('keydown', function(e) {
   checkKeys(e);
}); 

function checkKeys(event) {
  if(document.getElementById("pageNo").innerHTML.length >= 4){
    document.getElementById("pageNo").innerHTML = "P";
  }
  var x = event.key;
  document.getElementById("pageNo").innerHTML =          document.getElementById("pageNo").innerHTML + x;
}
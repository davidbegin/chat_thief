var newDiv = document.createElement('div');
newDiv.setAttribute("id", "pageNo");
var newContent = document.createTextNode("P100");
newDiv.append(newContent);
var currentDiv = document.getElementsByTagName("h1");
currentDiv = currentDiv[0];
document.body.insertBefore(newDiv, currentDiv);

document.addEventListener('keydown', function(e) {
   checkKeys(e);
}); 

function checkKeys(event) {
  var x = event.key;
  document.getElementById("pageNo").innerHTML = "P00"+x;
}
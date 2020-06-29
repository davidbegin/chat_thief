window.onload = addDivs;
function addDivs(){
  var d = new Date();
  var days = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"];
  var day = days[d.getDay()];
  var date = d.getDate();
  var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  var mon = months[d.getMonth()];
  var hrs = d.getHours();
  var mins = d.getMinutes();
  var newDiv = document.createElement('div');
  newDiv.setAttribute("id", "zanussClock");
  var newContent = document.createTextNode(hrs+":"+mins);
  newDiv.append(newContent);
  var currentDiv = document.getElementsByTagName("h1")[0];
  document.body.insertBefore(newDiv, currentDiv);
  var dateDiv = document.createElement('div');
  dateDiv.setAttribute("id", "zanussDayDate");
  var newContent = document.createTextNode(day + " " + date + " " + mon);
  dateDiv.append(newContent);
  var currentDiv = document.getElementsByTagName("h1")[0];
  document.body.insertBefore(dateDiv, currentDiv);
}
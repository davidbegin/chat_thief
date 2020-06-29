window.addEventListener("load", function() {
  var d = new Date();
  var days = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"];
  var day = days[d.getDay()];
  var date = d.getDate();
  var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  var mon = months[d.getMonth()];
  var hrs = d.getHours();
  var mins = d.getMinutes();
  if (mins<=9){mins = '0' + mins;}
  var clockDiv = document.createElement('div');
  clockDiv.setAttribute("id", "zanussClock");
  var clockContent = document.createTextNode(hrs+":"+mins);
  clockDiv.append(clockContent);
  var clockCurrentDiv = document.getElementsByTagName("h1")[0];
  document.body.insertBefore(clockDiv, clockCurrentDiv);
  var dateDiv = document.createElement('div');
  dateDiv.setAttribute("id", "zanussDayDate");
  var dateContent = document.createTextNode(day + " " + date + " " + mon);
  dateDiv.append(dateContent);
  var datecurrentDiv = document.getElementsByTagName("h1")[0];
  document.body.insertBefore(dateDiv, datecurrentDiv);
});
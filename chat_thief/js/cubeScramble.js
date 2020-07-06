window.addEventListener("load", function() {
  var movesChoices = ['F','R','U','B','L','D','F2','R2','U2','B2','L2','D2',"F'","R'","U'","B'","L'","D'"];
  var moves = [];
  for (var i=0; i<=19; i++){
    var random = Math.floor(Math.random() * 17);
    moves.push(movesChoices[random]); 
  }
  var scrambleText = "";
  for(var j=0; j<moves.length; j++){
    scrambleText += moves[j]
    if(j<moves.length-1){
      scrambleText += ", ";
    }
  }
  var scrambleDiv = document.createElement('div');
   scrambleDiv.setAttribute("id", "cubeScramble");
  var scrambleContent = document.createTextNode(scrambleText);
  scrambleDiv.append(scrambleContent);
  var findH1 = document.getElementsByTagName("h1")[0];
  document.body.insertBefore(scrambleDiv, findH1);
});
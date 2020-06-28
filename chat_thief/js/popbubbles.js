// This widget requires you to !buy bubbles
window.addEventListener("load", function() {
    // get an instance of sound to play
    var a = new Audio("../commands/aww.html")
    // pop bubbles on click
    for (i=0;i<=10;i++) {
        b = document.querySelector(".bubble x" + i);
        b.onclick = pop
        function pop () {
            event.target.remove();
            a.play();
        }
    }
});

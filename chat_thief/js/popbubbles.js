// This widget requires you to !buy bubbles
window.addEventListener("load", function() {
    bubbles = document.getElementsByClasName(".bubble")
    bubbles.map(b => b.onclick = pop)
    function pop () {
        // get an instance of sound to play
        var a = new Audio("../commands/aww.html")
        event.target.remove();
        a.play();
    }
});

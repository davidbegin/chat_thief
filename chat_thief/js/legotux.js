var h1s = document.getElementsByTagName("h1");

var matrix = document.createElement("canvas");
matrix.id = "matrix";
matrix.style="clear:both;position:fixed;left:0;top:0;width:100vw;height:100vh;";
document.body.insertBefore(matrix, h1s[0]);

const ctx2d = matrix.getContext('2d');

const width = matrix.width = document.body.offsetWidth;
const height = matrix.height = document.body.offsetHeight;
const cols = Math.floor(width / 20) + 1;
const yPos = Array(cols).fill(0);

ctx2d.fillStyle = '#fff1';
ctx2d.fillRect(0, 0, width, height);

function drawMatrix () {
	ctx2d.fillStyle = '#0001';
	ctx2d.fillRect(0, 0, width, height);
	ctx2d.fillStyle = '#0f0';
	ctx2d.font = '1em monospace';

	yPos.forEach((y, ind) => {
		const text = String.fromCharCode(Math.random() * 128);
		const x = ind * 20;
		ctx2d.fillText(text, x, y);
		if (y > 100 + Math.random() * 10000) yPos[ind] = 0;
		else yPos[ind] = y + 20;
	});
}

setInterval(drawMatrix, 100);
window.addEventListener('load', () => {
	const div = document.createElement('div')

	// Add the forbidden class, for added styling :)
	div.classList.add('forbidden-div') 
	div.style.position = 'fixed'

	div.innerHTML = 'The Forbidden &lt;div&gt;'

	document.body.appendChild(div)

	// Follow that mouse
	document.addEventListener("mousemove", (e) => {
		div.style.left = `${e.x - 24}px`
		div.style.top = `${e.y - 24}px`
	})
})

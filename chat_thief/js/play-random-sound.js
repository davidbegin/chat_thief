window.addEventListener('load', () => {
	let userCommands = []

	fetch('/db/commands.json').then(resp => resp.json()).then(json => {
		const USER = window.location.pathname.replace('.html', '').replace('/', '')
		const commands = [ ...Object.keys(json.commands) ].map(i => json.commands[i])

		userCommands = commands.filter(cmd => cmd.permitted_users.filter(user => user ===USER).length > 0)
	})

	const pickRandomCommand = commands => commands[Math.floor(Math.random() * commands.length)]

	const playSound = (e) => {
		const cmd = pickRandomCommand(userCommands)

		if (!cmd) {
			return
		}

		{new Audio(`/media/${cmd.name}.opus`).play()} 
		{new Audio(`/media/${cmd.name}.mpa`).play()} 
		{new Audio(`/media/${cmd.name}.m4a`).play()} 
		{new Audio(`/media/${cmd.name}.wav`).play()} 
	}

	document.addEventListener('keydown', playSound)
	document.addEventListener('mousedown', playSound)
})

import { roomLi, floorLi } from './templates.js'
;(async () => {
	// fetching initial data
	const rooms = await (await fetch('/rooms')).json()
	const roomRoot = document.querySelector('#room-root')
	for (const room of rooms) {
		roomRoot.innerHTML += roomLi(room)
	}
	const floors = await (await fetch('/floors')).json()
	const floorRoot = document.querySelector('#right-side')
	for (const floor of floors) {
		floorRoot.innerHTML += floorLi(floor)
	}

	// adding onClick event listener to each checkbox
	const checkboxes = document.querySelectorAll('input[type=checkbox]')
	for (const ele of checkboxes) {
		ele.addEventListener('click', async e => {
			e.preventDefault()
			const checked = e.target.checked

			const response = await fetch('/rooms', {
				body: JSON.stringify({ ID: Number(ele.dataset.roomId), on: checked }),
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				}
			})

			e.target.checked = response.ok ? checked : !checked
		})
	}

	// add onInput event listener to search bar
	document.querySelector('#search-bar').addEventListener('input', ({ target: { value } }) => {
		roomRoot.innerHTML = ''
		for (const room of rooms) {
			roomRoot.innerHTML += room.name.includes(value) ? roomLi(room) : ''
		}
	})

	// periodically updating states
	setInterval(async () => {
		let failed = false
		const response = await fetch('/rooms').catch(() => (failed = true))

		for (const ele of checkboxes) ele.disabled = failed
		if (failed) return

		const rooms = await response.json()
		for (const room of rooms) {
			for (const ele of checkboxes) {
				if (ele.dataset.roomId == room.ID) {
					ele.checked = room.on
					break
				}
			}
		}
	}, 500)
})()

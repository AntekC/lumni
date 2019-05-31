export const roomLi = ({ name, on, ID }) => `
	<li>
	${name.toUpperCase()}
		<input type="checkbox" class="switch" ${on && 'checked'}" data-room-id="${ID}"/>
	</li>
`

export const floorLi = ({ name }) => `
	<div class="menu-item">
		<div class="floor-name">${name.toUpperCase()}</div>
		<div id="scndFloor"></div>
	</div>
`

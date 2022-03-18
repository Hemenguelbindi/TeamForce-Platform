const menuButton = document.querySelector('.hamburger__btn');
let hamburger = document.querySelector('.hamburger');

if (menuButton) {
	menuButton.addEventListener('click', function(element) {
		hamburger.classList.toggle('active');
	})

	document.body.addEventListener('click', function(element) {
		if (hamburger.classList == 'active') {
			if (!element.target.closest('header')) {
				hamburger.classList.remove('active');
			}
		}
	})

	document.addEventListener('keydown', function(event) {
		if (hamburger.classList == 'active') {
			if (event.code == 'Escape') {
				hamburger.classList.remove('active');
			}
		}
	});
}
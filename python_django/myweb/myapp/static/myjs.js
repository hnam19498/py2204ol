// document.getElementById("i1").innerHTML = 'Test 1'
// document.getElementById('i2').innerHTML = "Test 2"
// document.getElementById('i3').innerHTML = 'Test 3'

$('.delete').on('click', function(event) {
	event.preventDefault();
	
	var choice = confirm(this.getAttribute('data-confirm'));

	if (choice) {
		window.location.href = this.getAttribute('href');
	}
})
var solid = '<i class="fa-solid"></i>';
var circle = '<i class="fa-solid fa-circle"></i>';
var crossedCircle = '<i class="fa-solid fa-circle-xmark"></i>';

var cells = document.getElementsByClassName('board_cell');

Array.prototype.forEach.call(cells, function(element) {
	element.addEventListener('click', function() {
      if (element.innerHTML == solid) {
        element.innerHTML = circle;
      }
      else if (element.innerHTML == circle) {
        element.innerHTML = crossedCircle;
      }
      else if (element.innerHTML == crossedCircle) {
        element.innerHTML = solid;
      }
	});
});
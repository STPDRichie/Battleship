// boards = document.getElementsByClassName('game_board');
icons = document.querySelectorAll('.fa-solid');

// cells.children.addEventListener('click', event => {
//   if
// })
// icon.forEach(element => {
  // element.getAttribute('class');
  // element.children.className = 'fa-solid fa-circle-xmark'
  // element.className
// })

// icon('click', event => {
//   if (icon.className == 'fa-solid'){
//     icon.className = 'fa-solid fa-circle'
//   }
//   else if (icon.className == 'fa-solid fa-circle') {
//     icon.className = 'fa-solid fa-circle-xmark'
//   }
// })

icons.array.forEach(element => {
  element.addEventListener('click', event => {
    if (element.className == 'fa-solid') {
      element.className = 'fa-solid fa-circle';
    }
    else if (element.className == 'fa-solid fa-circle') {
      element.className = 'fa-solid fa-circle-xmark';
    }
  })
});
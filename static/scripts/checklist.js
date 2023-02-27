const todoList = document.getElementById('todo-list');
const completedList = document.getElementById('completed-list');

todoList.addEventListener('click', function(event) {
  if (event.target.classList.contains('complete-btn')) {
    const confirmMessage = 'Are you sure you want to complete this item?';
    if (confirm(confirmMessage)) {
      const listItem = event.target.parentElement;
      todoList.removeChild(listItem);
      const completeButton = listItem.querySelector('.complete-btn');
      listItem.removeChild(completeButton);
      const undoButton = document.createElement('button');
      undoButton.innerText = 'Undo';
      undoButton.classList.add('undo-btn');
      listItem.appendChild(undoButton);
      const items = Array.from(completedList.querySelectorAll('li'));
      items.push(listItem);
      items.sort((a, b) => {
        const aStep = parseInt(a.querySelector('.step').innerText.slice(5));
        const bStep = parseInt(b.querySelector('.step').innerText.slice(5));
        return aStep - bStep;
      });
      completedList.innerHTML = '';
      items.forEach(item => {
        completedList.appendChild(item);
      });
    }
  }
});

completedList.addEventListener('click', function(event) {
  if (event.target.classList.contains('undo-btn')) {
    const confirmMessage = 'Are you sure you want to undo this item?';
    if (confirm(confirmMessage)) {
      const listItem = event.target.parentElement;
      completedList.removeChild(listItem);
      const undoButton = listItem.querySelector('.undo-btn');
      listItem.removeChild(undoButton);
      const completeButton = document.createElement('button');
      completeButton.innerText = 'Complete';
      completeButton.classList.add('complete-btn');
      listItem.appendChild(completeButton);
      const items = Array.from(todoList.querySelectorAll('li'));
      items.push(listItem);
      items.sort((a, b) => {
        const aStep = parseInt(a.querySelector('.step').innerText.slice(5));
        const bStep = parseInt(b.querySelector('.step').innerText.slice(5));
        return aStep - bStep;
      });
      todoList.innerHTML = '';
      items.forEach(item => {
        todoList.appendChild(item);
      });
    }
  }
});

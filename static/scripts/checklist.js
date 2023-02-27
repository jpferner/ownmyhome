// Add click event listener to complete buttons
document.querySelectorAll('.complete-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const id = btn.dataset.id;
    const row = btn.closest('tr');
    const data = {id: id};
    fetch('/complete-item', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Update row in To-Do table
        row.querySelector('.status').textContent = 'Completed';
        row.querySelector('.complete-btn').remove();
        // Move row to Completed table
        const completedList = document.querySelector('#completed-list');
        completedList.appendChild(row);
      } else {
        alert('Error completing item. Please try again later.');
      }
    })
    .catch(error => {
      console.error('Error completing item:', error);
      alert('Error completing item. Please try again later.');
    });
  });
});

// Add click event listener to undo buttons
document.querySelectorAll('.undo-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const id = btn.dataset.id;
    const row = btn.closest('tr');
    const data = {id: id};
    fetch('/undo-item', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Update row in Completed table
        row.querySelector('.status').textContent = 'Incomplete';
        row.querySelector('.undo-btn').remove();
        // Move row to To-Do table
        const todoList = document.querySelector('#todo-list');
        todoList.appendChild(row);
        // Add complete button to row
        const completeBtn = document.createElement('button');
        completeBtn.classList.add('complete-btn');
        completeBtn.dataset.id = id;
        completeBtn.textContent = 'Complete';
        row.querySelector('td:last-child').appendChild(completeBtn);
      } else {
        alert('Error undoing item. Please try again later.');
      }
    })
    .catch(error => {
      console.error('Error undoing item:', error);
      alert('Error undoing item. Please try again later.');
    });
  });
});


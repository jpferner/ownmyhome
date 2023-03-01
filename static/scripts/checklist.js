// Add event listeners to "Complete" and "Undo" buttons
var buttons = document.querySelectorAll('.complete-btn, .undo-btn');
for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', toggleStatus);
}

// Send AJAX request to toggle item status
function toggleStatus(event) {
  const id = event.target.getAttribute('data-id');
  const completed = event.target.getAttribute('data-completed') === 'true';
  fetch(`/toggle_status/${id}`, {
    method: 'POST',
    body: JSON.stringify({ completed: !completed }),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(() => {
    if (completed) {
      // Move item from completed to todo table
      const row = event.target.parentElement.parentElement;
      row.querySelector('.status').textContent = 'Incomplete';
      row.querySelector('button').className = 'complete-btn';
      row.querySelector('button').textContent = 'Complete';
      row.querySelector('button').setAttribute('data-completed', 'false');
      document.getElementById('todo-list').appendChild(row);
      // Sort the tables by step number
      const todoList = document.getElementById('todo-list');
      const completedList = document.getElementById('completed-list');
      const sortedTodo = Array.from(todoList.children).sort((a, b) => {
        const aStep = parseInt(a.querySelector('td').textContent.slice(5));
        const bStep = parseInt(b.querySelector('td').textContent.slice(5));
        return aStep - bStep;
      });
      const sortedCompleted = Array.from(completedList.children).sort((a, b) => {
        const aStep = parseInt(a.querySelector('td').textContent.slice(5));
        const bStep = parseInt(b.querySelector('td').textContent.slice(5));
        return aStep - bStep;
      });
      todoList.innerHTML = '';
      sortedTodo.forEach(item => todoList.appendChild(item));
      completedList.innerHTML = '';
      sortedCompleted.forEach(item => completedList.appendChild(item));
    } else {
      // Move item from todo to completed table
      const row = event.target.parentElement.parentElement;
      row.querySelector('.status').textContent = 'Completed';
      row.querySelector('button').className = 'undo-btn';
      row.querySelector('button').textContent = 'Undo';
      row.querySelector('button').setAttribute('data-completed', 'true');
      document.getElementById('completed-list').appendChild(row);
      // Sort the tables by step number
      const todoList = document.getElementById('todo-list');
      const completedList = document.getElementById('completed-list');
      const sortedTodo = Array.from(todoList.children).sort((a, b) => {
        const aStep = parseInt(a.querySelector('td').textContent.slice(5));
        const bStep = parseInt(b.querySelector('td').textContent.slice(5));
        return aStep - bStep;
      });
      const sortedCompleted = Array.from(completedList.children).sort((a, b) => {
        const aStep = parseInt(a.querySelector('td').textContent.slice(5));
        const bStep = parseInt(b.querySelector('td').textContent.slice(5));
        return aStep - bStep;
      });
      todoList.innerHTML = '';
      sortedTodo.forEach(item => todoList.appendChild(item));
      completedList.innerHTML = '';
      sortedCompleted.forEach(item => completedList.appendChild(item));
    }
  });
}

// Update the To-Do and Completed tables
function updateChecklists() {
  var todoList = document.getElementById('todo-list');
  var completedList = document.getElementById('completed-list');
  fetch('/get_checklists').then(response => {
    if (response.ok) {
      response.json().then(data => {
        // Sort the todo and completed tables by step number
        const sortedTodo = data.todo.sort((a, b) => a.order_no - b.order_no);
        const sortedCompleted = data.completed.sort((a, b) => a.order_no - b.order_no);
        // Clear existing table rows
        todoList.innerHTML = '';
        completedList.innerHTML = '';
        // Add updated table rows
        sortedTodo.forEach(item => {
          var row = createTableRow(item);
          todoList.appendChild(row);
        });
        sortedCompleted.forEach(item => {
          var row = createTableRow(item);
          completedList.appendChild(row);
        });
      });
    }
  });
}

// Helper function to create a table row from a checklist item
function createTableRow(item) {
    var row = document.createElement('tr');
    row.setAttribute('data-id', item.order_no);
    row.innerHTML = `
        <td>Step ${item.order_no}</td>
        <td>${item.detail}</td>
        <td class="status">${item.status ? 'Completed' : 'Incomplete'}</td>
        <td>
            <button class="${item.status ? 'undo-btn' : 'complete-btn'}" data-id="${item.order_no}" data-completed="${item.status}">
                ${item.status ? 'Undo' : 'Complete'}
            </button>
        </td>
    `;
    row.querySelector('button').addEventListener('click', toggleStatus);
    return row;
}

// Initialize the To-Do and Completed tables
updateChecklists();

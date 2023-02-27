// Get the To-Do and Completed tables
const todoList = document.getElementById('todo-list');
const completedList = document.getElementById('completed-list');

// Add event listeners to the Complete and Undo buttons
const completeButtons = document.querySelectorAll('.complete-btn');
completeButtons.forEach(button => {
    button.addEventListener('click', () => {
        const row = button.parentNode.parentNode;
        const id = row.getAttribute('data-id');
        const statusCell = row.querySelector('.status');

        // Update the status and move the row to the Completed table
        statusCell.textContent = 'Completed';
        todoList.removeChild(row);
        completedList.appendChild(row);

        // Add the Undo button
        const undoButton = document.createElement('button');
        undoButton.textContent = 'Undo';
        undoButton.setAttribute('data-id', id);
        undoButton.classList.add('undo-btn');
        const actionCell = button.parentNode;
        actionCell.appendChild(undoButton);

// Remove the Complete button and disable it
        button.remove();

// Add event listener to the Undo button
        undoButton.addEventListener('click', () => {
            const row = undoButton.parentNode.parentNode;
            const id = row.getAttribute('data-id');
            const statusCell = row.querySelector('.status');

            // Update the status and move the row back to the To-Do table
            statusCell.textContent = 'Incomplete';
            completedList.removeChild(row);
            todoList.appendChild(row);

            // Remove the Undo button and add the Complete button back
            undoButton.remove();
            const completeButton = document.createElement('button');
            completeButton.textContent = 'Complete';
            completeButton.setAttribute('data-id', id);
            completeButton.classList.add('complete-btn');
            actionCell.appendChild(completeButton);

            // Add event listener to the Complete button
            completeButton.addEventListener('click', () => {
                const row = completeButton.parentNode.parentNode;
                const id = row.getAttribute('data-id');
                const statusCell = row.querySelector('.status');

                // Update the status and move the row to the Completed table
                statusCell.textContent = 'Completed';
                todoList.removeChild(row);
                completedList.appendChild(row);

                // Add the Undo button and remove the Complete button
                const undoButton = document.createElement('button');
                undoButton.textContent = 'Undo';
                undoButton.setAttribute('data-id', id);
                undoButton.classList.add('undo-btn');
                actionCell.appendChild(undoButton);
                completeButton.remove();

                // Add event listener to the Undo button
                undoButton.addEventListener('click', () => {
                    const row = undoButton.parentNode.parentNode;
                    const id = row.getAttribute('data-id');
                    const statusCell = row.querySelector('.status');

                    // Update the status and move the row back to the To-Do table
                    statusCell.textContent = 'Incomplete';
                    completedList.removeChild(row);
                    todoList.appendChild(row);

                    // Remove the Undo button and add the Complete button back
                    undoButton.remove();
                    actionCell.appendChild(completeButton);
                });
            });
        });

    });
});

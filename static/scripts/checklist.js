function sortTableRows(table) {
    // Get all rows in the table body
    const rows = Array.from(table.tBodies[0].rows);

    // Sort rows by their step number
    rows.sort((row1, row2) => {
        const step1 = parseInt(row1.cells[0].textContent.match(/\d+/).toString());
        const step2 = parseInt(row2.cells[0].textContent.match(/\d+/).toString());
        return step1 - step2;
    });

    // Reinsert rows in sorted order
    rows.forEach(row => table.tBodies[0].appendChild(row));
}

const todoList = document.getElementById('todo-list');
const completedList = document.getElementById('completed-list');
const completeButtons = document.querySelectorAll('.complete-btn');

completeButtons.forEach(button => {
    button.addEventListener('click', () => {
        const row = button.parentNode.parentNode;
        const id = row.getAttribute('data-id');
        const statusCell = row.querySelector('.status');
        statusCell.textContent = 'Completed';
        todoList.removeChild(row);
        completedList.appendChild(row);
        sortTableRows(completedList.parentNode);
        const undoButton = document.createElement('button');
        undoButton.textContent = 'Undo';
        undoButton.setAttribute('data-id', id);
        undoButton.classList.add('undo-btn');
        const actionCell = button.parentNode;
        actionCell.appendChild(undoButton);
        button.remove();
        undoButton.addEventListener('click', () => {
            const row = undoButton.parentNode.parentNode;
            const id = row.getAttribute('data-id');
            const statusCell = row.querySelector('.status');
            statusCell.textContent = 'Incomplete';
            completedList.removeChild(row);
            todoList.appendChild(row);
            sortTableRows(todoList.parentNode);
            undoButton.remove();
            const completeButton = document.createElement('button');
            completeButton.textContent = 'Complete';
            completeButton.setAttribute('data-id', id);
            completeButton.classList.add('complete-btn');
            actionCell.appendChild(completeButton);
            completeButton.addEventListener('click', () => {
                const row = completeButton.parentNode.parentNode;
                completedList.appendChild(row);
                sortTableRows(completedList.parentNode);
                const undoButton = document.createElement('button');
                undoButton.textContent = 'Undo';
                undoButton.setAttribute('data-id', id);
                undoButton.classList.add('undo-btn');
                actionCell.appendChild(undoButton);
                completeButton.remove();
                undoButton.addEventListener('click', () => {
                    const row = undoButton.parentNode.parentNode;
                    const statusCell = row.querySelector('.status');
                    statusCell.textContent = 'Incomplete';
                    completedList.removeChild(row);
                    todoList.appendChild(row);
                    sortTableRows(todoList.parentNode);
                    undoButton.remove();
                    actionCell.appendChild(completeButton);
                });
            });
        });
    });
});

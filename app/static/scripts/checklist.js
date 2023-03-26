$(document).ready(function () {
    // Get the CSRF token from the meta tag in the header
    const csrf_token = $('meta[name=csrf-token]').attr('content');

    // When the complete button is clicked
    $('table').on('click', '.complete-btn', function () {
        const btn = $(this);
        const order_no = btn.data('id');

        // Send a POST request to update the item status in the database
        $.ajax({
            url: '/checklist',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrf_token
            },
            contentType: 'application/json',
            data: JSON.stringify({
                order_no: order_no,
                status: true
            }),
            success: function (response) {
                if (response.success) {
                    // Update the button and table row
                    btn.removeClass('complete-btn').addClass('undo-btn').text('Undo');
                    const row = btn.closest('tr');
                    row.find('.status').text('Completed');

                    // Find the correct position for the row in the completed list
                    const rows = $('#completed-list tr');
                    let inserted = false;
                    rows.each(function () {
                        const currentRow = $(this);
                        if (parseInt(currentRow.data('id')) > order_no) {
                            currentRow.before(row);
                            inserted = true;
                            return false;
                        }
                    });

                    // If the correct position wasn't found, append the row to the end of the list
                    if (!inserted) {
                        $('#completed-list').append(row);
                    }
                }
            }
        });
    });

    // When the undo button is clicked
    $('table').on('click', '.undo-btn', function () {
        const btn = $(this);
        const order_no = btn.data('id');

        // Send a POST request to update the item status in the database
        $.ajax({
            url: '/checklist',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrf_token
            },
            contentType: 'application/json',
            data: JSON.stringify({
                order_no: order_no,
                status: false
            }),
            success: function (response) {
                if (response.success) {
                    // Update the button and table row
                    btn.removeClass('undo-btn').addClass('complete-btn').text('Complete');
                    const row = btn.closest('tr');
                    row.find('.status').text('Incomplete');

                    // Find the correct position for the row in the todo list
                    const rows = $('#todo-list tr');
                    let inserted = false;
                    rows.each(function () {
                        const currentRow = $(this);
                        if (parseInt(currentRow.data('id')) > order_no) {
                            currentRow.before(row);
                            inserted = true;
                            return false;
                        }
                    });

                    // If the correct position wasn't found, append the row to the end of the list
                    if (!inserted) {
                        $('#todo-list').append(row);
                    }
                }
            }
        });
    });
});

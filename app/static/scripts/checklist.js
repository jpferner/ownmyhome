$(document).ready(function () {
    // Get the CSRF token from the meta tag in the header
    var csrf_token = $('meta[name=csrf-token]').attr('content');

    // When the complete button is clicked
    $('table').on('click', '.complete-btn', function () {
        var btn = $(this);
        var order_no = btn.data('id');
        var completed = btn.data('completed');

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
                    var row = btn.closest('tr');
                    row.find('.status').text('Completed');

                    // Find the correct position for the row in the completed list
                    var rows = $('#completed-list tr');
                    var inserted = false;
                    rows.each(function () {
                        var currentRow = $(this);
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
        var btn = $(this);
        var order_no = btn.data('id');
        var completed = btn.data('completed');

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
                    var row = btn.closest('tr');
                    row.find('.status').text('Incomplete');

                    // Find the correct position for the row in the todo list
                    var rows = $('#todo-list tr');
                    var inserted = false;
                    rows.each(function () {
                        var currentRow = $(this);
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

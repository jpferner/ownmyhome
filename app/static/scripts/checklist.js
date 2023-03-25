$(document).ready(function () {
  const csrf_token = $('meta[name="csrf-token"]').attr('content');

  function updateItemStatus(item_id, status) {
    const data = {
      item_id: item_id,
      status: status,
      csrf_token: csrf_token
    };

    $.ajax({
      type: "POST",
      url: "/checklist",
      contentType: "application/json",
      dataType: "json",
      data: JSON.stringify(data),
      success: function (response) {
        if (status) {
          moveToCompleted(item_id);
        } else {
          moveToToDo(item_id);
        }
      },
      error: function (error) {
        console.log("Error:", error);
      }
    });
  }

  function moveToCompleted(item_id) {
    const row = $(`tr[data-id="${item_id}"]`);
    const undoButton = createUndoButton(item_id);
    row.find(".complete-btn").replaceWith(undoButton);
    row.appendTo("#completed-list");
    sortList("#completed-list");
  }

  function moveToToDo(item_id) {
    const row = $(`tr[data-id="${item_id}"]`);
    const completeButton = createCompleteButton(item_id);
    row.find(".undo-btn").replaceWith(completeButton);
    row.appendTo("#todo-list");
    sortList("#todo-list");
  }

  function createCompleteButton(item_id) {
    const button = $(`<button class="complete-btn" data-id="${item_id}" data-completed="false">Complete</button>`);
    button.on("click", function () {
      updateItemStatus(item_id, true);
    });
    return button;
  }

  function createUndoButton(item_id) {
    const button = $(`<button class="undo-btn" data-id="${item_id}" data-completed="true">Undo</button>`);
    button.on("click", function () {
      updateItemStatus(item_id, false);
    });
    return button;
  }

  function sortList(listSelector) {
    $(listSelector)
      .children("tr")
      .sort((a, b) => {
        const stepA = parseInt($(a).data("id"));
        const stepB = parseInt($(b).data("id"));

        return stepA - stepB;
      })
      .appendTo(listSelector);
  }

  $(".complete-btn").on("click", function () {
    const item_id = $(this).data("id");
    updateItemStatus(item_id, true);
  });

  $(".undo-btn").on("click", function () {
    const item_id = $(this).data("id");
    updateItemStatus(item_id, false);
  });
});

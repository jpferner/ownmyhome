let container = document.querySelector(".container");

//global variables
const monthEl = $(".c-main");
const dataCel = $(".c-cal__cel");
const dateObj = new Date();
const month = dateObj.getMonth() + 1;
let day = dateObj.getDate();
let year = dateObj.getFullYear();
const monthText = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];
let indexMonth = month;
const todayBtn = $(".c-today__btn");
const addBtn = $(".js-event__add");
const saveBtn = $(".js-event__save");
const closeBtn = $(".js-event__close");
const winCreator = $(".js-event__creator");
const inputDate = $(this).data();
today = moment().format("YYYY-MM-DD");
let events = {};
let eventForm = {};
let selectedDay = moment().format("YYYY-MM-DD");
const currentEventId = 0;
const csrf_token = $("meta[name=csrf-token]").attr("content");

// ------ set default events -------

$(document).ready(function () {
  loadEvents();
});

/**
 * Loads events from the server using an AJAX GET request. On a successful response,
 * it processes the returned events, converts them into the required format, and stores
 * them in the events object. Finally, it calls updateEventList() to display the events.
 */
function loadEvents() {
  $.ajax({
    url: "/calendar/events",
    type: "GET",
    headers: {
      "X-CSRFToken": csrf_token,
    },
    success: function (response) {
      events = {};

      response.forEach(function (event) {
        const datetime = moment(event.time);
        const date = datetime.format("YYYY-MM-DD");
        const time = datetime.format("HH:mm:ss");

        const endDatetime = moment(event.endTime);
        const endTime = endDatetime.format("HH:mm:ss");

        if (!(date in events)) {
          events[date] = [];
        }
        events[date].push({
          id: event.id,
          name: event.name,
          notes: event.notes,
          date: date,
          time: time,
          endTime: endTime,
        });
      });
      updateEventList();
    },
  });
}

// ------ functions control -------

//button of the current day
todayBtn.on("click", function () {
  let step;
  if (month < indexMonth) {
    step = indexMonth % month;
    movePrev(step, true);
  } else if (month > indexMonth) {
    step = month - indexMonth;
    moveNext(step, true);
  }
  selectedDay = moment().format("YYYY-MM-DD");
  updateEventList();

  $(".c-aside__num").text(selectedDay.slice(8));
  $(".c-aside__month").text(monthText[month - 1]);

  dataCel.each(function () {
    if ($(this).data("day") === selectedDay) {
      $(this).addClass("isSelected");
      //fillEventSidebar($(this));
    } else {
      $(this).removeClass("isSelected");
    }
  });
  $(".js-event__add").show();
   $(".js-event__remove").show();
});

//highlight the cel of current day
dataCel.each(function () {
  if ($(this).data("day") === today) {
    $(this).addClass("isToday");
    $(this).addClass("isSelected");
    //fillEventSidebar($(this));
  }
});

/**
 *  Displays the event form by adding the isVisible class to the winCreator element and
 *  the overlay class to the body element. It also populates the form inputs with the data
 *  from the eventForm object.
 */
function openForm() {
  $("#event_form_error").text("");
  $("#event_form_error").removeClass("isVisible");
  winCreator.addClass("isVisible");
  $("body").addClass("overlay");
  document.querySelector('input[name="date"]').value = eventForm.date;
  document.querySelector('input[name="name"]').value = eventForm.name;
  document.querySelector('textarea[name="notes"]').value = eventForm.notes;
  document.querySelector('input[name="time"]').value = eventForm.time;
  document.querySelector('input[name="end_time"]').value = eventForm.endTime;
}

//window event creator
addBtn.on("click", function () {
  dataCel.each(function () {
    if ($(this).hasClass("isSelected")) {
      today = $(this).data("day");
    }
  });

  eventForm = {
    id: undefined,
    date: today,
    notes: "",
    name: "",
    time: "",
    endTime: "",
  };

  openForm();
});

closeBtn.on("click", function () {
  winCreator.removeClass("isVisible");
  $("body").removeClass("overlay");
});
saveBtn.on("click", function () {
  const inputName = $("input[name=name]").val();
  const inputDate = $("input[name=date]").val();
  const inputTime = $("input[name=time]").val();
  const inputEndTime = $("input[name=end_time]").val();
  const inputNotes = $("textarea[name=notes]").val();

  $.ajax({
    url:
      eventForm.id !== undefined
        ? "/calendar/events/" + eventForm.id
        : "/calendar/events",
    type: eventForm.id !== undefined ? "PUT" : "POST",
    headers: {
      "X-CSRFToken": csrf_token,
    },
    contentType: "application/json",
    data: JSON.stringify({
      name: inputName,
      notes: inputNotes,
      time: inputDate + "T" + inputTime + ".000000",
      endTime: inputDate + "T" + inputEndTime + ".000000",
    }),
    success: function (response) {
      if (eventForm.id !== undefined) {
        events[eventForm.date] = events[eventForm.date].filter(function (
          event
        ) {
          return event.id !== response.id;
        });
      }
      const datetime = moment(response.time);
      const date = datetime.format("YYYY-MM-DD");
      const time = datetime.format("HH:mm:ss");

      const endDatetime = moment(response.endTime);
      const endTime = endDatetime.format("HH:mm:ss");

      if (!(date in events)) {
        events[date] = [];
      }
      events[date].push({
        id: response.id,
        name: response.name,
        notes: response.notes,
        date: date,
        time: time,
        endTime: endTime,
      });
      updateEventList();

      winCreator.removeClass("isVisible");
      $("body").removeClass("overlay");
      $("#addEvent")[0].reset();
    },

    error: function (xhr, status, error) {
      let errorMessage = "";
      if (xhr.responseJSON.code === "OVERLAPPING_TIMES") {
        errorMessage = "Event times overlap with another event.";
      } else if (xhr.responseJSON.code === "INVALID_END_TIME") {
        errorMessage = "End time is before the start time.";
      } else if (xhr.responseJSON.code === "TIME_PAST_OCCURRENCE") {
        errorMessage = "Event time has already passed.";
      } else if (xhr.responseJSON.code === "NO_EVENT_NAME") {
        errorMessage = "Please enter a name for the event.";
      } else {
        errorMessage = "Unknown error occurred, please try again.";
      }
      $("#event_form_error").addClass("isVisible");
      $("#event_form_error").text(errorMessage);
    },
  });
});

/**
 * Updates the event list in the sidebar based on the selectedDay. It first clears
 * the event list and then adds events for the selected day sorted by time. For each event,
 * it appends the event information and buttons for removing and editing the event.
 */
function updateEventList() {
  $(".c-aside__eventList").empty();
  const currentDate = selectedDay;

  if (currentDate in events) {
    events[currentDate].sort(function (a, b) {
      return a.time.localeCompare(b.time);
    });

    events[currentDate].forEach(function (event) {
      $(".c-aside__eventList").append(
        "<div class='c-aside__event'>" +
          "<span class=c-aside__name>" +
          event.name +
          "</span>" +
          "<span> @ " +
          moment(event.time, "HH:mm:ss").format("h:mm A") +
          " - " +
          moment(event.endTime, "HH:mm:ss").format("h:mm A") +
          "</span>" +
          "<p>" +
          event.notes +
          "</p>" +
          "<div class='btn-group' role='group'>" +

          "<button type='button' name='remove' class='btn btn-outline-primary' onclick='removeEvent(this)' data-date='" +
          currentDate +
          "' data-id='" +
          event.id +
          "'><span class='fa fa-trash-o'></span></button>" +
          "<button type='button' name='edit' class='btn btn-outline-primary' onclick='editEvent(this)' data-date='" +
          currentDate +
          "' data-id='" +
          event.id +
          "'><span class='fa fas fa-edit'></span></button>" +
          "</div>" +
          "</div>"
      );
    });
  }
}

/**
 * Removes an event with the given eventId and eventDate from both the server using an AJAX DELETE
 * request and the events object. After removal, it calls updateEventList() to update the displayed events.
 * @param element
 */
function removeEvent(element) {
  const eventId = parseInt(element.getAttribute("data-id"));
  const eventDate = element.getAttribute("data-date");

  $.ajax({
    url: "/calendar/events/" + eventId,
    type: "DELETE",
    headers: {
      "X-CSRFToken": csrf_token,
    },
    success: function (response) {
      events[eventDate] = events[eventDate].filter(function (event) {
        return event.id !== eventId;
      });
      updateEventList();
    },
  });
}

/**
 * Prepares the event form for editing an event with the given eventId and eventDate.
 * It sets the eventForm object with the event's information and then calls openForm()
 * to display the event form.
 * @param element
 */
function editEvent(element) {
  const eventId = parseInt(element.getAttribute("data-id"));
  const eventDate = element.getAttribute("data-date");

  events[eventDate].forEach(function (event) {
    if (eventId === event.id) {
      eventForm = {
        id: event.id,
        name: event.name,
        notes: event.notes,
        date: event.date,
        time: event.time.substring(0, 5),
        endTime: event.endTime.substring(0, 5),
      };
    }
  });
  openForm();
}

dataCel.on("click", function () {
  const thisEl = $(this);
  const thisDay = $(this).attr("data-day").slice(8);
  const thisMonth = $(this).attr("data-day").slice(5, 7);

  //  fillEventSidebar($(this));
  selectedDay = year + "-" + thisMonth + "-" + thisDay;

  if (selectedDay < moment().format("YYYY-MM-DD")) {
    $(".js-event__add").hide();
    $(".js-event__remove").hide();
  } else {
    $(".js-event__add").show();
    $(".js-event__remove").show();
  }

  updateEventList();

  $(".c-aside__num").text(thisDay);
  $(".c-aside__month").text(monthText[thisMonth - 1]);

  dataCel.removeClass("isSelected");
  thisEl.addClass("isSelected");
});

/**
 * Moves the calendar view to the next month(s) by sliding the calendar to the left.
 * It takes two arguments: the number of months to move (fakeClick) and a boolean indicating
 * whether to update the indexMonth (indexNext).
 * @param fakeClick
 * @param indexNext
 */
function moveNext(fakeClick, indexNext) {
  for (let i = 0; i < fakeClick; i++) {
    $(".c-main").css({
      left: "-=100%",
    });
    $(".c-paginator__month").css({
      left: "-=100%",
    });
    switch (true) {
      case indexNext:
        indexMonth += 1;
        break;
    }
  }
}

/**
 * Moves the calendar view to the previous month(s) by sliding the calendar to the right.
 * It takes two arguments: the number of months to move (fakeClick) and a boolean indicating
 * whether to update the indexMonth (indexPrev).
 * @param fakeClick
 * @param indexPrev
 */
function movePrev(fakeClick, indexPrev) {
  for (let i = 0; i < fakeClick; i++) {
    $(".c-main").css({
      left: "+=100%",
    });
    $(".c-paginator__month").css({
      left: "+=100%",
    });
    switch (true) {
      case indexPrev:
        indexMonth -= 1;
        break;
    }
  }
}

/**
 * Sets up event listeners for the calendar paginator buttons. It takes five arguments:
 * the button's ID (buttonId), the main calendar class (mainClass), the paginator month class (monthClass),
 * and two booleans indicating whether the button is for moving to the next month (next) or the previous
 * month (prev).
 * @param buttonId
 * @param mainClass
 * @param monthClass
 * @param next
 * @param prev
 */
function buttonsPaginator(buttonId, mainClass, monthClass, next, prev) {
  switch (true) {
    case next:
      $(buttonId).on("click", function () {
        if (indexMonth >= 2) {
          $(mainClass).css({
            left: "+=100%",
          });
          $(monthClass).css({
            left: "+=100%",
          });
          indexMonth -= 1;
        }
        return indexMonth;
      });
      break;
    case prev:
      $(buttonId).on("click", function () {
        if (indexMonth <= 11) {
          $(mainClass).css({
            left: "-=100%",
          });
          $(monthClass).css({
            left: "-=100%",
          });
          indexMonth += 1;
        }
        return indexMonth;
      });
      break;
  }
}

buttonsPaginator("#next", monthEl, ".c-paginator__month", false, true);
buttonsPaginator("#prev", monthEl, ".c-paginator__month", true, false);

//launch function to set the current month
moveNext(indexMonth - 1, false);

//fill the sidebar with current day
$(".c-aside__num").text(day);
$(".c-aside__month").text(monthText[month - 1]);

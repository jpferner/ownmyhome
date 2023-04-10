let container = document.querySelector(".container");

//global variables
var monthEl = $(".c-main");
var dataCel = $(".c-cal__cel");
var dateObj = new Date();
var month = dateObj.getMonth() + 1;
var day = dateObj.getDate();
var year = dateObj.getFullYear();
var monthText = [
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
  "December"
];
var indexMonth = month;
var todayBtn = $(".c-today__btn");
var addBtn = $(".js-event__add");
var saveBtn = $(".js-event__save");
var closeBtn = $(".js-event__close");
var winCreator = $(".js-event__creator");
var inputDate = $(this).data();
today = moment().format("YYYY-MM-DD");
var events = {};
var eventForm = {};
var selectedDay = moment().format("YYYY-MM-DD");
var currentEventId = 0;
const csrf_token = $('meta[name=csrf-token]').attr('content');


// ------ set default events -------

$(document).ready(function () {
    loadEvents();
});

function loadEvents() {
     $.ajax({
            url: '/calendar/events',
            type: 'GET',
            headers: {
                'X-CSRFToken': csrf_token
            },
            success: function (response) {
                events = {};

                response.forEach(function (event) {
                    var datetime = moment(event.time)
                    var date = datetime.format("YYYY-MM-DD");
                    var time = datetime.format("HH:mm:ss");

                    var endDatetime = moment(event.endTime);
                    var endTime = endDatetime.format("HH:mm:ss");

                    if (!(date in events)) {
                        events[date] = [];

                    }
                    events[date].push({
                        id: event.id,
                        name: event.name,
                        notes: event.notes,
                        date: date,
                        time: time,
                        endTime: endTime
                    });

                });
                console.log(response);
                updateEventList();
            }
        });

}

// ------ functions control -------

//button of the current day
todayBtn.on("click", function() {
  if (month < indexMonth) {
    var step = indexMonth % month;
    movePrev(step, true);
  } else if (month > indexMonth) {
    var step = month - indexMonth;
    moveNext(step, true);
  }
  selectedDay = moment().format("YYYY-MM-DD");
  updateEventList();

  $(".c-aside__num").text(selectedDay.slice(8));
  $(".c-aside__month").text(monthText[month - 1]);

  dataCel.each(function() {
  if ($(this).data("day") === selectedDay) {
    $(this).addClass("isSelected");
    //fillEventSidebar($(this));
  }
  else {
    $(this).removeClass("isSelected");
  }
});
});

//highlight the cel of current day
dataCel.each(function() {
  if ($(this).data("day") === today) {
    $(this).addClass("isToday");
    $(this).addClass("isSelected");
    //fillEventSidebar($(this));
  }
});

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
addBtn.on("click", function() {
  dataCel.each(function() {
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
  endTime: ""
  }

  openForm();

});

closeBtn.on("click", function() {
  winCreator.removeClass("isVisible");
  $("body").removeClass("overlay");
});
saveBtn.on("click", function() {
  var inputName = $("input[name=name]").val();
  var inputDate = $("input[name=date]").val();
  var inputTime = $("input[name=time]").val();
  var inputEndTime = $('input[name=end_time]').val();
  var inputNotes = $("textarea[name=notes]").val();

  console.log(inputEndTime);


  $.ajax({

            url: eventForm.id !== undefined ? "/calendar/events/" + eventForm.id : "/calendar/events",
            type: eventForm.id !== undefined ? 'PUT' : 'POST',
            headers: {
                'X-CSRFToken': csrf_token
            },
            contentType: 'application/json',
            data: JSON.stringify({
                name: inputName,
                notes: inputNotes,
                time: inputDate + 'T' + inputTime + ".000000",
                endTime: inputDate + 'T' + inputEndTime + ".000000"
            }),
            success: function (response) {
                if (eventForm.id !== undefined) {
                    events[eventForm.date] = events[eventForm.date].filter(function (event) {
                        return event.id !== response.id;
                    });

                }
                var datetime = moment(response.time);
                var date = datetime.format("YYYY-MM-DD");
                var time = datetime.format("HH:mm:ss");

                var endDatetime = moment(response.endTime);
                var endTime = endDatetime.format("HH:mm:ss");


                if (!(date in events)) {
                    events[date] = [];

                }
                events[date].push({
                    id: response.id,
                    name: response.name,
                    notes: response.notes,
                    date: date,
                    time: time,
                    endTime: endTime
                });
                updateEventList();

                winCreator.removeClass("isVisible");
                $("body").removeClass("overlay");
                $("#addEvent")[0].reset();
            },

            error: function (xhr, status, error) {


                console.log(xhr.responseJSON);
                var errorMessage = "";
                if (xhr.responseJSON.code === "OVERLAPPING_TIMES") {
                    errorMessage = "Event times overlap with another event.";
                } else if (xhr.responseJSON.code === "INVALID_END_TIME") {
                    errorMessage = "End time is before the start time.";
                    console.log(errorMessage);
                } else {
                    errorMessage = "Unknown error occurred, please try again."
                }
                $("#event_form_error").addClass("isVisible");
                $("#event_form_error").text(errorMessage);
            }
  });

});


function updateEventList() {
  $(".c-aside__eventList").empty();
  const currentDate = selectedDay;


  if (currentDate in events) {
    events[currentDate].sort(function(a, b) {
        return a.time.localeCompare(b.time);
    });

    events[currentDate].forEach(function (event) {
        $(".c-aside__eventList").append(
            "<div class='c-aside__event'>" +
            event.name +
            " <span> @ " +
            moment(event.time, 'HH:mm:ss').format('h:mm A') + " - " + moment(event.endTime, 'HH:mm:ss').format('h:mm A') +
            "<p>" +
            event.notes +
            "</p>" +
            "<a class='c-add o-btn js-event__remove' onclick='removeEvent(this)' data-date='" + currentDate + "' data-id='" + event.id + "'>remove event <span class='fa fa-trash-o'></span></a>" +
            "<a class='c-add o-btn js-event__remove' onclick='editEvent(this)' data-date='" + currentDate + "' data-id='" + event.id + "'>edit event <span class='fa fa-trash-o'></span></a>" +

            "</span> </div>"

        );



    });
    console.log(events[currentDate]);
  }
  console.log(currentDate);

}

function removeEvent(element) {
    var eventId = parseInt(element.getAttribute("data-id"));
    var eventDate = element.getAttribute("data-date");

    $.ajax({
            url: '/calendar/events/' + eventId,
            type: 'DELETE',
            headers: {
                'X-CSRFToken': csrf_token
            },
            success: function (response) {
                events[eventDate] = events[eventDate].filter(function (event) {
                    return event.id !== eventId;
                });
                updateEventList();
            }
        });



}

function editEvent(element) {
    var eventId = parseInt(element.getAttribute("data-id"));
    var eventDate = element.getAttribute("data-date");

    events[eventDate].forEach(function (event) {
        if (eventId === event.id) {
            eventForm = {
                id: event.id,
                name: event.name,
                notes: event.notes,
                date: event.date,
                time: event.time.substring(0, 5),
                endTime: event.endTime.substring(0,5)
            };
        }
    });
    openForm();
}

dataCel.on("click", function() {
  var thisEl = $(this);
  var thisDay = $(this)
  .attr("data-day")
  .slice(8);
  var thisMonth = $(this)
  .attr("data-day")
  .slice(5, 7);

//  fillEventSidebar($(this));
  selectedDay = year + "-" + thisMonth + "-" + thisDay;

  if (selectedDay < today) {
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

//function for move the months
function moveNext(fakeClick, indexNext) {
  for (var i = 0; i < fakeClick; i++) {
    $(".c-main").css({
      left: "-=100%"
    });
    $(".c-paginator__month").css({
      left: "-=100%"
    });
    switch (true) {
      case indexNext:
        indexMonth += 1;
        break;
    }
  }
}
function movePrev(fakeClick, indexPrev) {
  for (var i = 0; i < fakeClick; i++) {
    $(".c-main").css({
      left: "+=100%"
    });
    $(".c-paginator__month").css({
      left: "+=100%"
    });
    switch (true) {
      case indexPrev:
        indexMonth -= 1;
        break;
    }
  }
}

//months paginator
function buttonsPaginator(buttonId, mainClass, monthClass, next, prev) {
  switch (true) {
    case next:
      $(buttonId).on("click", function() {
        if (indexMonth >= 2) {
          $(mainClass).css({
            left: "+=100%"
          });
          $(monthClass).css({
            left: "+=100%"
          });
          indexMonth -= 1;
        }
        return indexMonth;
      });
      break;
    case prev:
      $(buttonId).on("click", function() {
        if (indexMonth <= 11) {
          $(mainClass).css({
            left: "-=100%"
          });
          $(monthClass).css({
            left: "-=100%"
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

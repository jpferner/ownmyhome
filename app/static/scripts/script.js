let container = document.querySelector(".container");
//
//dycalendar.draw({
//   target:'#dycalendar',
//   dayformat: 'full',
//   type: 'month',
//   monthformat: 'full',
//   highlighttoday: true,
//   prevnextbutton: 'show'
//});

//global variables
var monthEl = $(".c-main");
var dataCel = $(".c-cal__cel");
var dateObj = new Date();
var month = dateObj.getUTCMonth() + 1;
var day = dateObj.getUTCDate();
var year = dateObj.getUTCFullYear();
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
today = year + "-" + month + "-" + day;
var events = {};
var selectedDay = moment().format("YYYY-MM-DD");
var currentEventId = 0;

// ------ set default events -------
function defaultEvents(dataDay,dataName,dataNotes,classTag){
  var date = $('*[data-day='+dataDay+']');
  date.attr("data-name", dataName);
  date.attr("data-notes", dataNotes);
  date.addClass("event");
  date.addClass("event--" + classTag);
}

//defaultEvents(today, 'YEAH!','Today is your day','important');
//defaultEvents('2022-12-25', 'MERRY CHRISTMAS','A lot of gift!!!!','festivity');
//defaultEvents('2022-05-04', "LUCA'S BIRTHDAY",'Another gifts...?','birthday');
//defaultEvents('2022-03-03', "MY LADY'S BIRTHDAY",'A lot of money to spent!!!!','birthday');


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
});

//higlight the cel of current day
dataCel.each(function() {
  if ($(this).data("day") === today) {
    $(this).addClass("isToday");
    fillEventSidebar($(this));
  }
});

//window event creator
addBtn.on("click", function() {
  winCreator.addClass("isVisible");
  $("body").addClass("overlay");
  dataCel.each(function() {
    if ($(this).hasClass("isSelected")) {
      today = $(this).data("day");
      document.querySelector('input[type="date"]').value = today;
    } else {
      document.querySelector('input[type="date"]').value = today;
    }
  });
});
closeBtn.on("click", function() {
  winCreator.removeClass("isVisible");
  $("body").removeClass("overlay");
});
saveBtn.on("click", function() {
  var inputName = $("input[name=name]").val();
  var inputDate = $("input[name=date]").val();
  var inputNotes = $("textarea[name=notes]").val();
  var inputTag = $("select[name=tags]")
    .find(":selected")
    .text();
    if (inputName != null) {
        $(this).attr("data-name", inputName);
      }
      if (inputNotes != null) {
        $(this).attr("data-notes", inputNotes);
      }
      $(this).addClass("event");
      if (inputTag != null) {
        $(this).addClass("event--" + inputTag);
      }
      if (inputDate != null) {
        $(this).attr("data-date", inputDate);
      }
      fillEventSidebar($(this));

  dataCel.each(function() {
    if ($(this).data("day") === inputDate) {

    }
  });

  winCreator.removeClass("isVisible");
  $("body").removeClass("overlay");
  $("#addEvent")[0].reset();
});

//fill sidebar event info
function fillEventSidebar(self) {
  $(".c-aside__event").remove();
  var thisName = self.attr("data-name");
  var thisNotes = self.attr("data-notes");
  var thisEvent = self.hasClass("event");
  var thisDate = self.attr("data-date");
//  console.log(thisDate);

  if (!(thisDate in events)) {
    events[thisDate] = [];

  }
  events[thisDate].push({
    name: thisName,
    notes: thisNotes,
    date: thisDate,
    id: currentEventId
  });
  currentEventId += 1;
  console.log(events);
  updateEventList();

//  switch (true) {
//    case thisImportant:
//      $(".c-aside__eventList").append(
//        "<p class='c-aside__event c-aside__event--important'>" +
//        thisName +
//        " <span> • " +
//        thisNotes +
//        "</span></p>"
//      );
//      break;
//    case thisBirthday:
//      $(".c-aside__eventList").append(
//        "<p class='c-aside__event c-aside__event--birthday'>" +
//        thisName +
//        " <span> • " +
//        thisNotes +
//        "</span></p>"
//      );
//      break;
//    case thisFestivity:
//      $(".c-aside__eventList").append(
//        "<p class='c-aside__event c-aside__event--festivity'>" +
//        thisName +
//        " <span> • " +
//        thisNotes +
//        "</span></p>"
//      );
//      break;
//    case thisEvent:
//      $(".c-aside__eventList").append(
//        "<p class='c-aside__event'>" +
//        thisName +
//        " <span> • " +
//        thisNotes +
//        "</span></p>"
//      );
//      break;
//   }
};

function updateEventList() {
  $(".c-aside__eventList").empty();
  const currentDate = selectedDay;
  if (currentDate in events) {
    events[currentDate].forEach(function (event) {
        $(".c-aside__eventList").append(
            "<p class='c-aside__event'>" +
            event.name +
            " <span> . " +
            event.notes +
            "<a class='c-add o-btn js-event__remove' onclick='removeEvent(this)' data-date='" + currentDate + "' data-id='" + event.id + "'>remove event <span class='fa fa-plus'></span></a>" +
            "</span> </p>"

        );



    });
    console.log(events[currentDate]);
  }
  console.log(currentDate);

}

function removeEvent(element) {
    var eventId = parseInt(element.getAttribute("data-id"));
    var eventDate = element.getAttribute("data-date");

    events[eventDate] = events[eventDate].filter(function (event) {
        return event.id !== eventId;
    })
    updateEventList();

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

import argparse

from selenium import webdriver
import pickle
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
from getpass import getpass

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time


def main(url):
    email = input("Enter email of existing OwnMyHome account: ")
    password = getpass("Enter password: ")

    firefox_binary = FirefoxBinary()
    driver = webdriver.Firefox(firefox_binary=firefox_binary)

    driver.get(url)

    time.sleep(1)

    email_box = driver.find_element(By.NAME, "email")
    email_box.send_keys(email)

    password_box = driver.find_element(By.NAME, "password_hash")
    password_box.send_keys(password)
    email_box.submit()

    time.sleep(1)

    # driver.session_id = session
    calendar = driver.find_element(By.XPATH, '//a[@href="/calendar"]')
    calendar.click()

    print("\nTEST ERRORS FOUND:\n")
    print("TEST1\t", test_interactive_calendar(driver))
    print("TEST2\t", test_edit_remove_events(driver))
    print("TEST3\t", test_event_error_checking(driver))
    print("TEST4\t", test_display_sorted_events(driver))


def test_interactive_calendar(driver):
    """
    Test for US #36
    Acceptance criteria:

        The calendar page consists of an embedded calendar that displays events for the user.
        An add event button should add events that the user can input for the calendar.
    """

    date = str((datetime.datetime.now() + datetime.timedelta(days=1)).date())

    add = driver.find_element(By.NAME, "add")
    add.click()

    fill_form(driver, {
        "name": "event1",
        "notes": "these are my notes.",
        "date": date,
        "time": "18:00",
        "end_time": "20:00"
    })

    # If form does not submit and close, the test fails
    try:
        save = driver.find_element(By.NAME, "save")
        save.click()

        driver.find_element(By.CSS_SELECTOR, ".c-event__creator.isVisible")
        assert False
    except:
        pass

    # If page does not contain c-cal__container and c-aside__eventList, the test fails
    try:
        driver.find_element(By.CLASS_NAME, "c-cal__container")
        driver.find_element(By.CLASS_NAME, "c-aside__eventList")
    except:
        assert False

    assert True


def test_edit_remove_events(driver):
    """
    Test for US #65
    Acceptance criteria:

        Events in the calendar have an edit event button for the user.
        Events in the calendar have a remove event button for the user.
        The current contents should be shown to the user for them to write to for editing.
    """

    date = str((datetime.datetime.now() + datetime.timedelta(days=2)).date())

    add = driver.find_element(By.NAME, "add")
    add.click()

    event_name = "event1"

    fill_form(driver, {
        "name": event_name,
        "notes": "these are my notes.",
        "date": date,
        "time": "18:00",
        "end_time": "20:00"
    })

    save = driver.find_element(By.NAME, "save")
    save.click()

    daycell = driver.find_element(By.XPATH, '//div[@data-day="' + date + '"]')
    daycell.click()

    edit = driver.find_element(By.NAME, "edit")
    edit.click()

    fill_form(driver, {
        "name": event_name,
        "notes": "these are my edited notes.",
        "date": date,
        "time": "17:00",
        "end_time": "20:00"
    })

    # If event form does not submit and close, the test fails
    try:
        save = driver.find_element(By.NAME, "save")
        save.click()

        driver.find_element(By.CSS_SELECTOR, ".c-event__creator.isVisible")
        assert False
    except:
        pass

    # If event does not get removed from the display, the test fails
    try:
        remove = driver.find_element(By.NAME, "remove")
        remove.click()

        if driver.find_elements(By.NAME, "name").text == event_name:
            assert False
    except:
        pass

    assert True


def test_event_error_checking(driver):
    """
    Test for US #94
    Acceptance criteria:

        The back end of the calendar must check if the user entered times that overlap with another event or has an end time that is earlier than a start time.
        If true, the back end must assert an error code and not enter anything into the database.
        The calendar must display an error message for the user.
    """

    date = str((datetime.datetime.now() + datetime.timedelta(days=3)).date())

    add = driver.find_element(By.NAME, "add")
    add.click()

    fill_form(driver, {
        "name": "event1",
        "notes": "these are my notes.",
        "date": date,
        "time": "18:00",
        "end_time": "20:00"
    })

    save = driver.find_element(By.NAME, "save")
    save.click()

    error_data = [{
        "name": "event2",
        "notes": "these are my notes.",
        "date": date,
        "time": "18:00",
        "end_time": "17:00"
    },
        {
            "name": "event1",
            "notes": "these are my notes.",
            "date": date,
            "time": "17:00",
            "end_time": "19:00"
        },
        {
            "name": "event2",
            "notes": "these are my notes.",
            "date": date,
            "time": "18:00",
            "end_time": "20:00"
        },
        {
            "name": "event1",
            "notes": "these are my notes.",
            "date": date,
            "time": "19:00",
            "end_time": "21:00"
        },
        {
            "name": "",
            "notes": "these are my notes.",
            "date": date,
            "time": "12:00",
            "end_time": "13:00"
        },
        {
            "name": "event1",
            "notes": "these are my notes.",
            "date": str((datetime.datetime.now() + datetime.timedelta(days=-1)).date()),
            "time": "12:00",
            "end_time": "13:00"
        },
        {
            "name": "event1",
            "notes": "these are my notes.",
            "date": datetime.datetime.now().strftime('%m/%d/%Y'),
            "time": (datetime.datetime.now() + datetime.timedelta(hours=-1)).time().strftime('%H:%M'),
            "end_time": (datetime.datetime.now() + datetime.timedelta(hours=1)).time().strftime('%H:%M')
        }
    ]

    add = driver.find_element(By.NAME, "add")
    add.click()

    for error in error_data:

        fill_form(driver, error)

        save = driver.find_element(By.NAME, "save")
        save.click()

        # print(driver.find_element(By.CSS_SELECTOR, "#event_form_error.isVisible").text)

        # If form does not display errors thrown by backend, the test fails
        try:
            driver.find_element(By.CSS_SELECTOR, "#event_form_error.isVisible")
            driver.find_element(By.CSS_SELECTOR, ".c-event__creator.isVisible")

        except:
            assert False

    close = driver.find_element(By.NAME, "close")
    close.click()

    assert True


def test_display_sorted_events(driver):
    """
    Test for US #95
    Acceptance criteria:

        The calendar page must display events in some sort of listed format for the day selected.
        The beginning of the list must start with the earliest event descending to the latest event.
    """

    date = str((datetime.datetime.now() + datetime.timedelta(days=4)).date())

    unsorted_data = [{
            "name": "event1",
            "notes": "these are my notes.",
            "date": date,
            "time": "18:00",
            "end_time": "19:00"
        },
        {
            "name": "event2",
            "notes": "these are my notes.",
            "date": date,
            "time": "20:00",
            "end_time": "23:00"
        },
        {
            "name": "event3",
            "notes": "these are my notes.",
            "date": date,
            "time": "15:00",
            "end_time": "17:00"
        }]

    for event in unsorted_data:
        add = driver.find_element(By.NAME, "add")
        add.click()

        fill_form(driver, event)

        save = driver.find_element(By.NAME, "save")
        save.click()

    daycell = driver.find_element(By.XPATH, '//div[@data-day="' + date + '"]')
    daycell.click()

    stored_events = driver.find_elements(By.CLASS_NAME, "c-aside__name")

    # If the contents of the event list don't match the event data sorted by time, the test fails
    for i in range(len(unsorted_data)):
        if stored_events[i].text != sorted(unsorted_data, key=lambda d: d['time'])[i]['name']:
            assert False
    assert True


def fill_form(driver, event):
    """
    Helper method for filling event forms
    """

    name = driver.find_element(By.NAME, "name")
    name.clear()
    name.send_keys(event['name'])

    date = driver.find_element(By.NAME, "date")
    date.clear()
    date.send_keys(event['date'])

    time = driver.find_element(By.NAME, "time")
    time.clear()
    time.send_keys(event['time'])

    end_time = driver.find_element(By.NAME, "end_time")
    end_time.clear()
    end_time.send_keys(event['end_time'])

    notes = driver.find_element(By.NAME, "notes")
    notes.clear()
    notes.send_keys(event['notes'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='System test for OwnMyHome calendar page\n'
                                                 'Existing account must be provided with no calendar events')
    # parser.add_argument('-e', '--email', metavar='email', required=True,
    #                     help='email for existing OwnMyHome account')
    # parser.add_argument('-p', '--password', metavar='password', required=True,
    #                     help='password for existing OwnMyHome account')
    parser.add_argument('url', metavar='url',
                        help='url used for local testing (e.g. localhost:5000)')
    args = parser.parse_args()
    main(args.url)



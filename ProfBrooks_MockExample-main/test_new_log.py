from new_log import do_something_interesting
import logging
import requests
import pytest
import new_log

@pytest.fixture
def activity_log_mocker(mocker):
    mocker.patch('new_log.log_event')


def test_something_interesting(activity_log_mocker):
    assert do_something_interesting()
    new_log.log_event.assert_called_once()


def test_event_log_logs_to_info_when_success(mocker):
    mocker.patch("logging.info")
    response = requests.Response()
    response.status_code = 201

    mocker.patch.object(requests, "post", return_value=response)
    new_log.log_event(1, "john", "testing success")
    requests.post.assert_called_once()
    logging.info.assert_called_once()


def test_event_log_logs_to_critical_when_failed_response(mocker):
    mocker.patch("logging.critical")
    response = requests.Response()
    response.status_code = 404

    mocker.patch.object(requests, "post", return_value=response)
    new_log.log_event(1, "john", "testing success")
    requests.post.assert_called_once()
    logging.critical.assert_called_once()


def test_event_log_logs_to_critical_when_exception(mocker):
    mocker.patch("logging.critical")
    response = requests.Response()
    response.status_code = 404

    mocker.patch.object(
        requests,
        "post",
        side_effect=requests.exceptions.RequestException
    )
    new_log.log_event(1, "john", "testing success")
    requests.post.assert_called_once()
    URL = 'http://localhost:5001'
    logging.critical.assert_called_once_with(
        f"Could not connect to activity log service at {URL}"
    )

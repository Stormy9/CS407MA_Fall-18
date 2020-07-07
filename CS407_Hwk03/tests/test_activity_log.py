#examples from the 'Part 2 - Mocking' Prof Brooks video
from app import activity_log_list, activity_log_id, new_wolfit_activity, do_something
import pytest
import requests
import logging


def test_something():
	assert do_something()


# it's all good, but the really good stuff starts @13:12+/-  (:
#	and 14:56 (it's a long one this time!)
#
#
# don't forget to make a cov.sh file and make it executable

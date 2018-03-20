#!/usr/bin/env python3
import datetime, time

def now_datetime():
	return datetime.datetime.now()

def now_timestamp():
    now = now_datetime()
    date = datetime.datetime(now.year, now.month, now.day, 9, 0, 0)
    timestamp = date.strftime("%s")
    return timestamp

def get_timestamp_for_the_next_day():
	now = now_datetime()
	if (now.hour < 6):
		date = datetime.datetime(now.year, now.month, now.day, 9, 0, 0)
		timestamp = date.strftime("%s")
	else:
		date = datetime.datetime(now.year, now.month, now.day+1, 9, 0, 0)
		timestamp = date.strftime("%s")
	return timestamp
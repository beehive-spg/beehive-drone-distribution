#!/usr/bin/env python3
import datetime, time

def get_timestamp_for_the_next_day():
	now = datetime.datetime.now()
	if (now.hour < 6):
		date = datetime.datetime(now.year, now.month, now.day, 9, 0, 0)
		timestamp = date.strftime("%s")
	else:
		date = datetime.datetime(now.year, now.month, now.day+1, 9, 0, 0)
		timestamp = date.strftime("%s")
	return timestamp
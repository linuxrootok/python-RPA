# -*-coding:utf-8-*-
import time

STANDARD_TIME_TUPLE = (2019, 3, 25, 0, 0, 0, 0, 0, 0)
STANDARD_TIME = int(time.mktime(STANDARD_TIME_TUPLE))
SECONDS_OF_HOUR = 3600
SECONDS_OF_DAY = 86400
SECONDS_OF_WEEK = 604800


def mill_second():
	return int(time.time() * 1000)


def second():
	return int(time.time())


def get_hour_no(i=0):
	if not i:
		i=second()
	return int((i-STANDARD_TIME)/SECONDS_OF_HOUR) + 1


def get_day_no(i=0):
	if not i:
		i=second()
	return int((i-STANDARD_TIME)/SECONDS_OF_DAY) + 1


def get_week_no(i=0):
	if not i:
		i=second()
	return int((i-STANDARD_TIME)/SECONDS_OF_WEEK) + 1


def get_month_no(i=0):
	if not i:
		i=second()
	time_tuple = time.localtime(i)	
	return ((time_tuple[0] - STANDARD_TIME_TUPLE[0]) * 12 
		+ (time_tuple[1] - STANDARD_TIME_TUPLE[1]) + 1)

"""
	获取下个周期的时间
"""


def get_second_by_hour_no(no):
	return STANDARD_TIME + SECONDS_OF_HOUR * (no - 1)


def get_second_by_day_no(no):
	return STANDARD_TIME + SECONDS_OF_DAY * (no - 1)


def get_second_by_week_no(no):
	return STANDARD_TIME + SECONDS_OF_WEEK * (no - 1)


def get_second_by_month_no(no):
	year = int(no / 12)
	month = no % 12 - 1
	t = STANDARD_TIME_TUPLE
	return int(time.mktime((t[0] + year, t[1] + month, t[2], t[3], t[4], t[5], t[6], t[7], t[8])))


if __name__ == "__main__":
	print(get_hour_no())
	print(get_day_no())
	print(get_week_no())
	print(get_month_no())
#!/usr/bin/env python3
from task_publisher import TTP

def main():
	setup()
	test_task_publisher()

def setup():
	global ttp
	ttp = TTP('{ "id":22 }')

def test_task_publisher():
	i=0
	while (i<10):
		ttp.start_queue()
		ttp.send_message()
		i+=1
	ttp.close_connection()

if __name__ == '__main__':
    main()
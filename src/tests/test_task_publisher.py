from task_publisher import TTP

test_task_publisher = TTP()
i=0
while (i<10):
	test_task_publisher.start_queue()
	test_task_publisher.send_message()
	test_task_publisher.send_log()
	i+=1
test_task_publisher.close_connection()
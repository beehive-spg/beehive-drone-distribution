from task_publisher import TTP

test_task_publisher = TTP()
test_task_publisher.start_queue()
test_task_publisher.send_message()
test_task_publisher.send_log()
import pymqi

# MQ connection details
queue_manager = 'QM1'
channel = 'DEV.APP.SVRCONN'
host = 'localhost'
port = '1414'
queue_name = 'DEV.QUEUE.1'
conn_info = f'{host}({port})'

# Connect to MQ
qmgr = pymqi.connect(queue_manager, channel, conn_info)

# Open queue for put and browse
queue = pymqi.Queue(qmgr, queue_name)



for i in range(3):
    # Create a message
    message = f'Test message {i + 1}'
    
    # Put the message on the queue
    queue.put(message)
    print(f"Put message: {message}")



# Clean up
queue.close()
qmgr.disconnect()
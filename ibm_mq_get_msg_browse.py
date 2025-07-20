import pymqi

# MQ connection details
queue_manager = 'QM1'
channel = 'DEV.APP.SVRCONN'
host = 'localhost'
port = '1414'
queue_name = 'DEV.QUEUE.1'
conn_info = f'{host}({port})'

# Connect to the queue manager
qmgr = pymqi.connect(queue_manager, channel, conn_info)

# Open queue with browse permission
open_options = pymqi.CMQC.MQOO_BROWSE | pymqi.CMQC.MQOO_INPUT_AS_Q_DEF
queue = pymqi.Queue(qmgr, queue_name, open_options)

# Set initial GMO for browse
gmo = pymqi.GMO()
gmo.Options = pymqi.CMQC.MQGMO_BROWSE_FIRST | pymqi.CMQC.MQGMO_NO_WAIT

print(f"Browsing messages in '{queue_name}':\n")

while True:
    try:
        # Create a fresh MD for every call
        md = pymqi.MD()
        
        message = queue.get(None, md, gmo)
        print("➤", message.decode('utf-8', errors='ignore'))

        # Switch to browse next
        gmo.Options = pymqi.CMQC.MQGMO_BROWSE_NEXT | pymqi.CMQC.MQGMO_NO_WAIT

    except pymqi.MQMIError as e:
        if e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
            print("\n✅ Done browsing — no more messages.")
            break
        else:
            print(f"❌ MQ Error: {e}")
            break

# Clean up
queue.close()
qmgr.disconnect()

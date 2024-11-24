from python_aternos import Client
import time

aternos = Client.from_credentials('SETASABA', 'SETASABA')
servs = aternos.list_servers()
eventserv = servs[1]


eventserv.start()
print("starting")

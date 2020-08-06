# Importing System Modules 
import socket
import sys
import os
import tkinter as tk
from functools import partial
from tkinter import filedialog

# Importing Custom Modules
import validIP

# Global Variables
ready = False
ourPort = tk.StringVar(tk.Tk())
ipAddress = tk.StringVar(tk.Tk())
port = 0
BUFFER_SIZE = 4096


# Definition of socket
print('Sock')
try:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except:
    print("Error in creation of socket")

# Begin Socket
def createSocket():
    global sock, port
    port = 50000
    try:
        sock.bind(('',port))
        print("Success")
    except:
        print('Error in bind') 

# Begin Functions of File Transfer
def recieve(peer):
    fileLoction = filedialog.askdirectory(title = 'Select the Location to Download')
    len = int(peer.recv(1000).decode())
    [fileName,size] = peer.recv(len).decode().split('<>')
    size = int(size)
    peer.send('Ack'.encode())
    if peer.recv(4).decode() != 'Ack':
        # Display Error
        sys.exit()
    # Recieve File
    with open(fileLoction+'/'+fileName,'wb') as f:
        bytes = peer.recv(BUFFER_SIZE)
        f.write(bytes)
    peer.close()

def send(peer):
    # Choose File
    file = filedialog.askopenfilename()
    fileName = file.split('/')[-1]
    size = os.path.getsize(file.read())
    temp = fileName+'<>'+str(size)
    peer.send(len(temp).encode())
    peer.send(temp.encode())
    if peer.recv(4).decode() != 'Ack':
        # Display Error
        sys.exit()
    peer.send('Ack'.encode())
    # Send File
    with open(file,"rb") as f:
        bytes = f.read(BUFFER_SIZE)
        peer.sendall(bytes)
    peer.close()






# Begin Functions of GUIs'
def connect():
    global sock, ipAddress, port
    conn = tk.Tk()
    conn.title('PyZap-Connection')
    conn.iconbitmap('pyzap.ico')
    # Verifying IP Adrress and Port Number
    if not validIP.verifyIP(ipAddress):
        #print('Not a valid IP') Display in Message Box
        sys.exit()
    if not validIP.VerifyPort(port):
        #print('Not a valid Port Number') Display in Message Box
        sys.exit()
    # Establishing a Connection
    sock.connect((ipAddress,port))
    if sock.recv(10) != 'Ack':
        # Disconnect from Peer
        sock.close()
    sock.send('Ack')
    tk.Button(conn,text = 'Send',command = send)
    tk.Button(conn,text = 'Recieve', command = recieve)


def beginRequest():
    global ipAddress, port
    conn = tk.Tk()
    conn.title('PyZap-Request')
    conn.iconbitmap('pyzap.ico')
    # Obtaining IP Adrress
    tk.Label(conn, text = 'Enter the IP Address to which you wish to connect').grid(row = 2, column = 0)
    tk.Entry(conn, textvariable = ipAddress).grid(row = 2, column = 2)
    # Obtainnig Port Number
    tk.Label(conn, text = 'Enter the Port Number to which you wish to connect').grid(row = 4, column = 0)
    tk.Entry(conn, textvariable = port).grid(row = 4,column = 2)
    
def beginAccept():
    global sock
    conn = tk.Tk()
    conn.title('PyZap-Accept')
    conn.iconbitmap('pyzap.ico')
    sock.listen(5)
    while True:
        peer, addr = sock.Accept()
        # Display the Peer details 
        peer.send('Ack')
        if peer.recv(10) != 'Ack':
            # Disconnect from Peer
            peer.close()
    tk.Button(conn,text = 'Send',command = send)
    tk.Button(conn,text = 'Recieve', command = partial(recieve,peer))

        




# Begin Base GUI
root = tk.Tk()
root.title('PyZap')
root.iconbitmap('pyzap.ico')
# To initiate the socket
tk.Button(root, text = 'CLick the button to start the service',command = createSocket).grid(row = 1, column = 0)

# To verify that the other Peer is ready 
tk.Button(root,text = 'Request',command = beginRequest).grid(row = 6, column = 1)
tk.Button(root,text = 'Accept',command = beginAccept).grid(row = 6, column = 3)
    
root.mainloop()

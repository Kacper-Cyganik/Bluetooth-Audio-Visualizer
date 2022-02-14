import bluetooth
from utils import show_menu, YouTube
from config import PORT,ADDRESS

# Bluetooth Client
def BluetoothClient():
    pause = False
    # Connect to Bluetooth 
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((ADDRESS, PORT))
    while True:
        
        show_menu()

        msg = input("Choose option: ")

        if msg == "X" or msg == "x":
            break
        
        if msg == "P" or msg == "p":
            if pause == False:
                print("Paused...")
            else:
                print("Playing...")
            pause = not pause
        # Increase volume
        if msg == "+":
            print("increasing volume")
        # Decrease volume
        if msg == "-":
            print("decreasing volume")

        # Send message
        sock.send(msg.encode())

        if msg == 'T' or msg == 't':
            search_title = input("Input Song title: ")
            result = YouTube(search_title)
            print("Now Playing...")
            print("title: ", result['title'])
            print("author: ", result['channel'])
            sock.send(search_title.encode())

    #close connection
    sock.close()

BluetoothClient()

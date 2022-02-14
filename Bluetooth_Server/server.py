from extend_func import *
import pafy
import vlc
import bluetooth
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

# play audio by finding Youtube url
def play_vlc(result, ins, player):
    result_url = result['url']
    try:
        video = pafy.new(result_url)
    except:
        player_start()
    streams = video.allstreams
    playurl = streams[1].url
    Media = ins.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.play()

# Main menu, display data on SH1106
def player_start():
    # Connect to SH1006
    serial = i2c(port=1, address=0x3C)
    device = sh1106(serial)

    # Init Bluetooth connection
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    server_sock.bind(("", port))
    server_sock.listen(1)
    client_socket, addr = server_sock.accept()
    print("Socket successfully created")

    # Init VLC
    ins = vlc.Instance()
    player = ins.media_player_new()
    player.audio_set_volume(80)
    pause = False

    result = None
    while True:

        # Receive message from client
        Select = client_socket.recv(1024)
        Select = Select.decode()

        # Search for music
        if Select == 'T' or Select == 't':
            search = client_socket.recv(1024)
            result = YouTube(search)
            print('Title:', result['title'], "\nChannel: ",
                  result['channel'], "\nviews: ", result['views'])
            play_vlc(result, ins, player)
        # Pause/Resume
        elif Select == 'P' or Select == 'p':
            player.set_pause(pause)
            pause = not pause
        # Increase Volume
        elif Select == '+':
            if player.audio_get_volume() <= 90:
                player.audio_set_volume(player.audio_get_volume()+5)
        # Decrease Volume
        elif Select == '-':
            if player.audio_get_volume() >= 10:
                player.audio_set_volume(player.audio_get_volume()-5)
        # Close
        elif Select == 'X' or Select == 'x':
            server_sock.close()
            client_socket.close()
            player.stop()
            exit(0)
        # Display status on SH1106
        with canvas(device) as draw:
            if result != None:
                title = result['title']
                if len(title) > 18:
                    title = result['title'][:19]+"\n-"+result['title'][19:]
                draw.text((5, 0), title.encode('utf-8'), fill="white")
                author = "By "+str(result['channel'])
                draw.text((15, 35), author.encode('utf-8'), fill="white")
                if pause == False:
                    draw.text((5, 50), 'Playing |', fill="white")
                else:
                    draw.text((5, 50), 'Paused |', fill="white")
                volume = "Vol: "+str(player.audio_get_volume())+"%"
                draw.text((65, 50), volume, fill="white")

from threading import Thread
from server import player_start
from led_matrix import led_matrix_start
from time import sleep
if __name__ == '__main__':
    Thread(target=led_matrix_start).start()
    sleep(5)
    Thread(target=player_start).start()
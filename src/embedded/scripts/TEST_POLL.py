import uselect
import sys
import time

poller = uselect.poll()
poller.register(sys.stdin, uselect.POLLIN)

if __name__ == "__main__":

    while True:
        if poller.poll(0):
            print(sys.stdin.readline())
            # print(sys.stdin.readline())

        time.sleep(0.01)
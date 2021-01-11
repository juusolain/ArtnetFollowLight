import socket
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

UDP_IP = config['listener'].get('addr')
UDP_PORT = 6454

universe = config['listener'].getint('universe')

paused = False

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, addr = sock.recvfrom(1024)
        process_packet(data, addr)
        
def process_packet(data, addr):
    global paused, universe
    header = data[0:7]
    # Check if artnet packet
    if not header == b'Art-Net':
        return
    # Parse packet
    opcode = int.from_bytes(data[8:9], byteorder="little")
    protver = int.from_bytes(data[10:11], byteorder="big")
    uni = int.from_bytes(data[14:15], byteorder="little")
    length = int.from_bytes(data[16:17], byteorder="big")
    level = data[18]
    if not uni == universe:
        return
    # Is paused
    if level < 128:
        paused = True
    # Not paused
    if level >= 128:
        paused = False



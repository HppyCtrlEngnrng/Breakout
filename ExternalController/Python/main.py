from socket import socket, AF_INET, SOCK_DGRAM
import struct
import numpy

def Angle180(a):
    if ( a < 180 ):
        return a;
    else:
        return a - 360;

remoteport = 7000;
localport = 7001;
addr = "127.0.0.1";

snd = 0.0;
K_dist = -20.0;
K_angle = 10.0;
K_ang_vel = 1.0;
flags = 0;
ang_prev = 0.0;
dt = 1/20.0;

sock = socket(AF_INET, SOCK_DGRAM);
sock.bind(('', localport));

while True:
    rcvd = sock.recvfrom(remoteport);
    rcvd = rcvd[0];
    
    if ( len(rcvd) >= 13 ):
        pos_ref = struct.unpack('<f', rcvd[0:4])[0];
        base_pos = struct.unpack('<f', rcvd[4:8])[0];
        pole_angle = Angle180(struct.unpack('<f', rcvd[8:12])[0]);
        flags = rcvd[12];
        
    if ( flags & 0x20 ):
        break;
    if ( flags & 0x80 ):
        ang_prev = 0.0;
        
    ang_vel = (pole_angle - ang_prev) / dt;
    snd = K_dist*(pos_ref - base_pos) - K_angle*pole_angle - K_ang_vel * ang_vel;

    sock.sendto(struct.pack('<f', numpy.float32(snd)), (addr, remoteport));
    
    ang_prev = pole_angle;
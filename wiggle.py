#!/usr/bin/env pypy
# for use with https://github.com/CarlosGS/grblForCyclone
import os
import sys
import time
import serial
import socket
import random
import threading

# 1.5 - movement from 90 to down position
# -3.8 movement quantity from 
# 8.5 left right

# Z : left/right
# Y : up/down

## command generators
def ponder(queue, mili):
    queue.append("G4 P{0}".format(str(mili)))
        
def upward(queue, step, rate):
    queue.append("G1 Y-{0} F{1}".format(str(step), str(rate)))
    queue.append("G4 P0.01")
        
def downward(queue, step, rate):
    queue.append("G1 Y{0} F{1}".format(str(step), str(rate)))
    queue.append("G4 P0.01")
        
def leftward(queue, step, rate):
    queue.append("G1 Z{0} F{1}".format(str(step), str(rate)))
    queue.append("G4 P0.01")
        
def rightward(queue, step, rate):
    queue.append("G1 Z-{0} F{1}".format(str(step), str(rate)))
    queue.append("G4 P0.01")

milli_timestamp = lambda: int(round(time.time() * 1000))
def getData(conn, sync, timing):
    writing=False
    tid=0
    datafile=0
    while True:
        try:
            if sync["sync"] == True and writing == False:
                datafile = open('{0}.dmp'.format(sync["name"]), 'wb')
                sync["sync"] = False
                writing = True
                tid = milli_timestamp()
                
            ts = milli_timestamp()

            data = conn.recv(1024)
            if not data and datafile != 0:
                datafile.close()
                datafile = 0
                break
            
            if (ts - tid) < timing and writing == True and datafile != 0:
                datafile.write(data)
                
            elif datafile != 0:
                if not datafile.closed:
                    datafile.close()
                    datafile = 0
                    writing = False
        except Exception as e:
            print("Shit on fire,yo!")
            print(e)
            datafile.close()
            datafile = 0
            break
    return

    
def runThread(Sync):
    sock = socket.socket( socket.AF_INET, # Internet       
                          socket.SOCK_DGRAM) # UDP
    sock.bind(("0.0.0.0", 9000))
    
    threading.Thread(target=getData, args=[sock, Sync, 250]).start()
    print("[Listening on port 9000]")
    return

    
if __name__ == "__main__":

    SAMPLE = { "sync": False,
               "name": "" }
    
    ## Build the command buffer
    random.seed(os.urandom(128))
    stamp = random.randint(1337,13371337)
    cycles = 280   # 70cycles is 90degrees
    steps = 80
    cmdStream = []
    cmdStream.append("G0 G91")

    for i in xrange(cycles):
        cmdStream.append( "#[Cycle "+ str(i+1) +"]" )
        if i/2 == i/2.0:
            for U in xrange(steps-1):
                upward(cmdStream, 0.0475, 40)
                cmdStream.append("!SAMPLE_{0}_{1}_{2}".format(str(stamp), str(i), str(U+1)) )
                ponder(cmdStream, 0.25)
        else:
            for D in xrange(steps-1):
                downward(cmdStream, 0.0475, 40)
                cmdStream.append("!SAMPLE_{0}_{1}_{2}".format(str(stamp), str(i), str(D+1)) )
                ponder(cmdStream, 0.25)
        leftward(cmdStream, 0.125, 50)
        cmdStream.append("!SAMPLE_{0}_{1}_{2}".format(str(stamp), str(i), str(0)) )
        ponder(cmdStream, 0.25)
        
    ##################################
    # Start telling grbl what to do! #
    ##################################
    
    s = serial.Serial('/dev/ttyACM0',115200)
    
    runThread(SAMPLE) # start the UDP-to-sample-files thread
    
    # Wake up, grbl!
    s.write("$X\n")
    s.write("\r\n\r\n")
    s.write("$x\n")
    s.write("$X\n")
    print 'starting in...'
    for sec in xrange(10):
        time.sleep(1)   # Wait for grbl to initialize
        print str(10 - sec) + '...'
    print 'GO!'
    s.flushInput()  # Flush startup text in serial input
    s.write("$X\n")
    
    # Stream g-code to grbl
    for line in cmdStream:
        if line[0] == "#":         # Declare the cycle we're on
            print line[1:]
            continue
        elif line[0] == "!":       # Trigger starting to write samples to a file
            SAMPLE["name"]=line[1:]
            SAMPLE["sync"]=True
            continue
        
        l = line.strip()           # Strip all EOL characters for streaming
        print('Sending: ' + l + '\n')
        s.write(l + '\n')          # Send g-code block to grbl
        grbl_out = s.readline()    # Wait for grbl response with carriage return
        print(' : ' + grbl_out.strip())
        
    # Wait here until grbl is finished to close serial port and file.
    raw_input("  Press <Enter> to exit and disable grbl.")

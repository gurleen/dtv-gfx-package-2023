import serial
from pydak.daktronics import Daktronics, DakSerial, dakSports
import socketio
import inflection

PORT = "/dev/cu.usbserial-120"
STOP_SEQ = [b'\x16', b'\x17']

def main():
    ser = serial.Serial(PORT, 19200, timeout=1, parity=serial.PARITY_NONE, rtscts=False, dsrdtr=False, xonxoff=False)
    dakserial = DakSerial(ser)
    dak = Daktronics("wrestling", dakserial)
    with socketio.SimpleClient() as sio:
        sio.connect("https://livestats.gurleen.dev")
        def update(key, value):
            print(f"{key} = {value}")
            sio.emit("do_update", {"key": key, "value": value})
        while True:
            dak.update()
            for item in dakSports["wrestling"].keys():
                if item != "dakSize":
                    val = dak[item].strip()
                    if not val:
                        continue
                    # print(f"{item}: {val}")
                    if item == "1 Main Clock Time (mm:ss/ss.t)":
                        update("Clock", val)
                    elif item == "30 Period":
                        update("Period", inflection.ordinalize(val))
                    elif item == "49 Home Advantage Text":
                        show = val == "ADVANTAGE"
                        update("show:Home-Riding-Time", show)
                        update("show:Away-Riding-Time", not show)
                    elif item == "52 Guest Advantage Text":
                        show = val == "ADVANTAGE"
                        update("show:Away-Riding-Time", show)
                        update("show:Home-Riding-Time", not show)
                    elif item == "41 Home Advantage Time (mm:ss)":
                        update("Home-Riding-Time", val)
                    elif item == "42 Guest Advantage Time (mm:ss)":
                        update("Away-Riding-Time", val)
                    elif item == "53 Home Match Score":
                        update("Home-Score", val)
                    elif item == "54 Guest Match Score":
                        update("Away-Score", val)

                    
    

def decode(ser):
    while True:
        c = ser.read()
        if c in STOP_SEQ:
            decode(line)
            decoded = line.decode("ascii").strip()
            # if line is not whitespace
            if decoded:
                pass
            line = b''
            continue
        line += c

if __name__ == "__main__":
    main()
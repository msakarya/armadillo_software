from bzrlib.doc_generate.autodoc_bash_completion import preamble
#!/usr/bin/env python
try:
    import serial
except:
    print("Please install PySerial\n")
    print("http://pyserial.sourceforge.net/index.html \n")    

class COM:
    def __init__(self,read_cbf=None):
        self.serial=serial.Serial()
        self.port="/dev/ttyUSB0"
        self.baudrate=115200
        
        self.read_cbf=read_cbf
        self.preamble=[0x55,0xAA]
        self.address=[73]
    def connect(self):
        print("Connecting to "+self.port)
        self.serial.port=self.port
        self.serial.baudrate=self.baudrate        
        try:
            self.serial.open()
        except:
            print("Can't open serial port")
    def disconnect(self):
        print("Closing "+self.port)
        if self.serial.isOpen():
            self.serial.close()
    def write(self,data):
        txpack=self.pack(data[:])
        if self.serial.isOpen():
            self.serial.write(txpack)
        else:
            print(txpack)
            print(self.depack(txpack))
    def pack(self,data=None):
        size=[len(data)]
        sum=0
        for d in data:
            sum=(sum+d)%256
        sum=[256-sum]
        txpack=self.preamble[:]+self.address[:]+size[:]+data[:]+sum[:]
        return txpack[:]
    def depack(self,data=None):
        pack_size=len(data)
        rxdata=None
        if(pack_size>5):
            preamble=data[0:2]
            address=data[2:3]            
            if((preamble==self.preamble)and(address==self.address)):
                size=data[3]                
                if (pack_size==(size+5)):
                    sum=0
                    rxdata=data[4:4+size]                    
                    for d in rxdata:
                        sum=(sum+d)%256
                    sum=256-sum                    
                    if(sum!=data[pack_size-1]):
                        rxdata=None

        return rxdata

if __name__=="__main__":
    com=COM()

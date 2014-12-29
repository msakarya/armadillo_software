#!/usr/bin/env python
__copyright__ = 'Copyright (C) 2010 Mustafa Sakarya'
__author__    = 'Mustafa Sakarya mustafasakarya1986@gmail.com'
__license__   = 'GNU GPLv3 http://www.gnu.org/licenses/'

from com import COM
import re
from http import Network
class ADC:
    def __init__(self):
        self.adc=range(32)
    def parse_adc(self,data):
        if(data[1]=='n'and(len(data)==18)):
            self.adc=range(8)
            adc_temp=bytearray(data[2:])            
            for i in range(8):
                self.adc[i]=adc_temp[i*2]*256+adc_temp[i*2+1]
        if(data[1]=='d'and(len(data)>18)):
            self.adc=range(32)
            adc_temp=bytearray(data[2:])
            for i in range(32):
                self.adc[i]=adc_temp[i*2]*256+adc_temp[i*2+1]
class SERVO:
    def __init__(self):
        self.s_pos=range(32)
        self.s_velocity=range(32)
        for i in range(32):
            self.s_pos[i]=120
            self.s_velocity[i]=0
    def pack_servo(self,which):
        w=which
        l=[]
        l.append(ord('s'))
        l.append(w)
        l.append(self.s_pos[w])
        l.append(self.s_velocity[w])        
        return l
    def s_set_value(self,which,pos,velocity=None):
        w=which
        self.s_pos[w]=pos
        self.s_velocity[w] = velocity if velocity else 0
        l=self.pack_servo(w)
        self.com.write(l)        
        return l


      
        
class Armadillo(ADC,SERVO):
    def __init__(self):
               
        ADC.__init__(self)
        SERVO.__init__(self)
        self.com=COM(read_cbf=self.parse)
        self.nlast=None
        n=self.network=Network(self.ncbf,self)
              
        
        self.d={}
        self.f={}
        f=self.f
        d=self.d
        d['request_id']="id?\r"
        d['ledset']="$t=l,a=" #task = ledset, args = ...
        f['message']=None
        f['seconds']=None
        f['adc']=None
        f['osf']=[] #one shot functions to be called
                    #at sync with com checkout
    def ncbf(self,data):
        t=data[0]
        n=self.network
        d=self.d
        if n.timer.cnt>20:            
            n.timer.interval=3
        elif n.timer.cnt>200:
            n.timer.cnt=201
            n.timer.interval=10
        if self.nlast!=data[0]:
            self.nlast=data[0]
            n.timer.cnt=0
            n.timer.interval=1
            task=data[1]
            if task=="ledset":
                print "ledset",data[2]
                if self.com.serial.isOpen():
                    self.com.write(d['ledset']+data[2])
    def parse(self,data):
        d=self.d
        f=self.f
        if(data[0]=='s'):
            if(len(data)>12):                
                s=''.join(data)
                s=re.split('[^0-9]', s)
                if(f['seconds']):
                    f['seconds'](s)
        elif(data[0]=='$'):
            s=''.join(data)
            if(f['message']):
                f['message'](s)
        elif(data[0]=='a'): #adc
            self.parse_adc(data)            
            if(f['adc']):
                f['adc'](self.adc)
            for f in f['osf']:               
                f()
            self.f['osf']=[]
    def connect(self):
        self.com.connect()
    def disconnect(self):
        self.com.disconnect()
    def destroy(self):
        try:
            #self.network.kill()
            self.com.disconnect()
        except:
            pass
    
    def request_id(self):
        d=self.d
        #print self.com.is_open()
        if self.com.serial.isOpen():
            self.com.write(d['request_id'])
class Kit:  #Name wrapper class
    def __init__(self):
        self.__kit__=Armadillo()
        k=self.__kit__
        self.connect=k.connect
        self.destroy=k.destroy
        self.disconnect=k.disconnect
        self.d=k.d # data
        self.f=k.f # functions
        self.register=k.network.register
        self.network=k.network
if __name__=="__main__":
    kit=Armadillo()
    kit.connect()
    n=kit.network
    n.connect()
    #kit.network.write("text")

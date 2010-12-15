#!/usr/bin/env python
__copyright__ = 'Copyright (C) 2010 Mustafa Sakarya'
__author__    = 'Mustafa Sakarya mustafasakarya1986@gmail.com'
__license__   = 'GNU GPLv3 http://www.gnu.org/licenses/'

import sys,os
"""
pyelectronics_path='/home/mustafa/work/projects/armadillo_software/gui/pyelectronics'
if not os.path.isdir(pyelectronics_path):
    print pyelectronics_path+' not found'
    sys.exit()
sys.path.append(pyelectronics_path)
print sys.path
"""
from pyelectronics import Armadillo

def main():
    kit=Armadillo()
    kit.connect()
    print kit.s_pos[3]
    print ('kit')
    kit.destroy()
    

if __name__=='__main__':
    main()
    print('main')

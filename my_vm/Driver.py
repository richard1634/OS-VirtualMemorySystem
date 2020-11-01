# -*- coding: utf-8 -*-
import Manager
class Driver:
   def __init__(self):

       manager = Manager.Manager()

       f = open("/Users/richardle/Desktop/init.txt", "r")
       line1 = f.readline() #ST Line 1: s1 z1 f1 s2 z2 f2 … sn zn fn
       line2 = f.readline() #PT Line 2: s1 p1 f1 s2 p2 f2 … sm pm fm
       line1 = line1.rstrip()
       line2 = line2.rstrip()
       line1 = line1.split(" ")
       line2 = line2.split(" ")

       manager.init_pm(line1,line2)

       va = open("/Users/richardle/Desktop/input.txt", "r")
       va_line1 = va.readline()
       va_line1 = va_line1.split(" ")

       open("/Users/richardle/Desktop/output.txt","w").close()

       for va in va_line1:
           manager.translate(int(va),"/Users/richardle/Desktop/nodp_output.txt")



       #f = open() something that reads all the VAs
test = Driver()

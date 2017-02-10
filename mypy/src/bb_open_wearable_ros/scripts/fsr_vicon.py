#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from bb_open_wearable_ros.msg import FsrDataMsg
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from time import sleep

import numpy as np

mux_sel_pin = "P9_25"
vicon_sync_pin="P9_24"
num_fsr_channels=6;
pub_freq=60;
bSync=False

mux_freq= '250' 
# Sensor connected to P9_40

def pin_setup():


    #falling edge detect for vicon sync pin
    GPIO.setup(vicon_sync_pin, GPIO.IN)
    GPIO.add_event_detect(vicon_sync_pin, GPIO.BOTH)
  #  GPIO.add_event_detect(vicon_sync_pin, GPIO.RISING)
    
    # mux select to be out .. May need  to be PWM
    GPIO.setup(mux_sel_pin, GPIO.OUT)

    #ADC set up
    ADC.setup()

def fsr_ADC_read():
    global num_fsr_channels
    fsr_vals=np.zeros(num_fsr_channels)

    GPIO.output(mux_sel_pin,GPIO.HIGH)
    # FSR is muxed only into 3 AI inputs 2,3,4
    fsr_vals[0]=ADC.read("AIN2")
    fsr_vals[1]=ADC.read("AIN3")
    fsr_vals[2]=ADC.read("AIN4")
    
    sleep(0.250) #wait 250ms
    
    GPIO.output(mux_sel_pin,GPIO.LOW)
    fsr_vals[3]=ADC.read("AIN2")
    fsr_vals[4]=ADC.read("AIN3")
    fsr_vals[5]=ADC.read("AIN4")

    return fsr_vals

def run_node():    
    global mux_sel_pin 
    global vicon_sync_pin
    global pub_freq
    global bSync
    pub = rospy.Publisher('bb_fsr', FsrDataMsg)
    rospy.init_node('bb_fsr_vicon')
    r = rospy.Rate(pub_freq) # 60hz

    
    
    FsrDataMsg_1=FsrDataMsg()
    FsrDataMsg_1.frame_id='beaglebone'
    while not rospy.is_shutdown():

        #set mux_sel to high for testing
        #GPIO.output(mux_sel_pin,GPIO.HIGH)
        #PWM.start(channel, duty, freq=2000, polarity=0)
        #PWM.start(mux_sel_pin, 50, mux_freq, 0)

        # vicon status will be triggered by sync pin falling edge
        if GPIO.event_detected(vicon_sync_pin) and bSync == False:
          rospy.loginfo("Sync detected")
          FsrDataMsg_1.vicon_Status= 1;
          bSync=True
        
        if GPIO.event_detected(vicon_sync_pin) and bSync == True:
          rospy.loginfo("Sync de -Triggered")
          FsrDataMsg_1.vicon_Status= 0;
          bSync=False
          
        # read ADC inputs   
        FsrDataMsg_1.fsr_vals=fsr_ADC_read()


        sent_msg = "Vicon: %s  FSR: %s %s %s " % (FsrDataMsg_1.vicon_Status, FsrDataMsg_1.fsr_vals[0], FsrDataMsg_1.fsr_vals[1],FsrDataMsg_1.fsr_vals[2])
        rospy.loginfo(sent_msg)
        
        FsrDataMsg_1.header.stamp = rospy.Time.now()
        pub.publish(FsrDataMsg_1)
        #rospy.sleep(1.0)
        r.sleep()


if __name__ == '__main__':
    try:
        pin_setup()
        run_node()
    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from bb_open_wearable_ros.msg import FsrDataMsg
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import numpy as np

mux_sel_pin = "P9_25"
vicon_sync_pin="P9_24"
num_fsr_channels=6;
pub_freq=60;
bSync=False
# Sensor connected to P9_40

def pin_setup():


    #falling edge detect for vicon sync pin
    GPIO.setup(vicon_sync_pin, GPIO.IN)
    GPIO.add_event_detect(vicon_sync_pin, GPIO.FALLING)

    # mux select to be out .. May need  to be PWM
    GPIO.setup(mux_sel_pin, GPIO.OUT)

    #ADC set up
    ADC.setup()

def fsr_ADC_read():
    global num_fsr_channels
    fsr_vals=np.zeros(num_fsr_channels)

    # FSR is muxed only into 3 AI inputs 2,3,4
    fsr_vals[0]=ADC.read("AIN2")
    fsr_vals[1]=ADC.read("AIN3")
    fsr_vals[3]=ADC.read("AIN3")

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

    while not rospy.is_shutdown():

        #set mux_sel to high for testing
        GPIO.output(mux_sel_pin,GPIO.HIGH)


        # vicon status will be triggered by sync pin falling edge
        if GPIO.event_detected(vicon_sync_pin) and bSync == False:
          rospy.loginfo("Sync detected")
          FsrDataMsg_1.vicon_Status= 1;
          bSync=True

        # read ADC inputs   
        FsrDataMsg_1.fsr_vals=fsr_ADC_read()


        sent_msg = "Vicon: %s  FSR: %s %s %s " % (FsrDataMsg_1.vicon_Status, FsrDataMsg_1.fsr_vals[0], FsrDataMsg_1.fsr_vals[1],FsrDataMsg_1.fsr_vals[2])
        rospy.loginfo(sent_msg)
        
        pub.publish(FsrDataMsg_1)
        #rospy.sleep(1.0)
        r.sleep()


if __name__ == '__main__':
    try:
        pin_setup()
        run_node()
    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from bb_open_wearable_ros.msg import FsrDataMsg

import numpy as np



def fsr_ADC_read():
    
    pub = rospy.Publisher('bb_fsr', FsrDataMsg)
    rospy.init_node('bb_fsr_vicon')
    r = rospy.Rate(60) # 60hz

    while not rospy.is_shutdown():
        FsrDataMsg_1=FsrDataMsg()
        # fsr_vals_temp=np.zeros(6)
        # fsr_vals_temp[2]=33;
        FsrDataMsg_1.fsr_vals[3]=44;

        FsrDataMsg_1.vicon_Status=6


        cad= "Vicon: %s  FSR: %s %s %s " % (FsrDataMsg_1.vicon_Status, FsrDataMsg_1.fsr_vals[0], FsrDataMsg_1.fsr_vals[1],FsrDataMsg_1.fsr_vals[2])
        rospy.loginfo(cad)
        
        pub.publish(FsrDataMsg_1)
        #rospy.sleep(1.0)
        r.sleep()


if __name__ == '__main__':
    try:
        
        fsr_ADC_read()
    except rospy.ROSInterruptException:
        pass

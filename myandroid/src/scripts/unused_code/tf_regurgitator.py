#!/usr/bin/env python
# -*- coding: utf-8 -*-
#"""
#Created on Wed Jun 24 21:48:52 2015
#
#@author: vijeth
#"""


import rospy
import tf2_ros
import geometry_msgs.msg


tango_topic='/tf'
          



source_frame ="start_of_service"
child_frame_id ="device"


if __name__ == '__main__':
    rospy.init_node('tf2_listener')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    tango_ss_pub = rospy.Publisher('tango_start_frame', geometry_msgs.msg.TransformStamped, queue_size=1)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform('device', 'start_of_service', rospy.Time(0))
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

        
        #msg = makePoseMsg(trans)    
        tango_ss_pub.publish(trans)    
        rospy.loginfo('published tf')
        rate.sleep()
    

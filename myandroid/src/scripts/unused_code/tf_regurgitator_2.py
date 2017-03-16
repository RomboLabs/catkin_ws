#!/usr/bin/env python
# -*- coding: utf-8 -*-
#"""
#Created on Wed Jun 24 21:48:52 2015
#
#@author: vijeth
#"""

import rospy
import message_filters
import os, datetime, sys

import tf2_ros
import tf2_msgs.msg

import geometry_msgs
from sensor_msgs.msg import Imu
from geometry_msgs.msg import TransformStamped
from bb_open_wearable_ros.msg import FsrDataMsg

mydir = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))
subjectName=[]
tango_counter=0;
vicon_counter=0;
mustAnnotate = True;

tango_tf_topic='/tf'

vicon_pose_topic='/vicon/tango7/mainBody'
tango_start_topic='tango_start_frame'
beagle_topic='/bb_fsr'
android_imu_topic='android/imu'


          



source_frame ='start_of_service'
child_frame_id ='device'

def sync_start_vicon_beagle_callback(tango_pose_start_device_msg,bb_fsr_msg,imu_msg):
     
         global tango_counter;
         global vicon_counter;
         

         
         print ' Relocalized...synced and saving frame',tango_pose_start_device_msg.header.frame_id;
         print "tango", tango_pose_start_device_msg.header.stamp.secs,tango_pose_start_device_msg.header.stamp.nsecs;
         print "beagle",bb_fsr_msg.header.stamp.secs,bb_fsr_msg.header.stamp.nsecs;  
         print "Imu",imu_msg.header.stamp.secs,imu_msg.header.stamp.nsecs;
         
if __name__ == '__main__':
    rospy.init_node('tf2_listener')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    tango_ss_pub = rospy.Publisher(tango_start_topic, geometry_msgs.msg.TransformStamped, queue_size=1)
    
    # message filter subsribers 
    #fs, queue_size, slop)¶
    tango_sub_start= message_filters.Subscriber(tango_start_topic, TransformStamped) #start to device 
    #vicon_sub= message_filters.Subscriber(vicon_pose_topic,TransformStamped )  # Vicon pose est 
    beagle_sub= message_filters.Subscriber(beagle_topic,FsrDataMsg )
    android_imu_sub=message_filters.Subscriber(android_imu_topic,Imu )
    
    rate = rospy.Rate(100.0)
    rospy.loginfo('Listening')
    while not rospy.is_shutdown():
        try:
            #from_frame,to_frame
            trans = tfBuffer.lookup_transform(source_frame, child_frame_id, rospy.Time(0))
            tango_ss_pub.publish(trans)    
            #rospy.loginfo('published tf')
            #message filter sync params
            ts_ = message_filters.ApproximateTimeSynchronizer([tango_sub_start,beagle_sub,android_imu_sub], 1,1)

             #message filter callbacks 
            ts_.registerCallback(sync_start_vicon_beagle_callback)

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

        
       
        
        rate.sleep()
    

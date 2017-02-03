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

from geometry_msgs.msg import TransformStamped
from bb_open_wearable_ros.msg import FsrDataMsg

mydir = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))
subjectName=[]
tango_counter=0;
vicon_counter=0;
mustAnnotate = True;

vicon_pose_topic='/vicon/tango7/mainBody'
tango_topic='/tf'
beagle_topic='/bb_fsr'



def sync_adf_only_callback(tango_pose_adf_device,vicon_pose):
     rospy.loginfo("synced");
     global tango_counter;
     global vicon_counter;
     global mydir;
    
             
     tango_adf_file=open(os.path.join(mydir,'tango_pose_adf'),'a')
     vicon_adf_file =open(os.path.join(mydir,'vicon_pose_adf'),'a')

     tango_adf_file.write(str(tango_pose_adf_device.status_code.status)+','+ str(tango_pose_adf_device.header.stamp.secs)+ ','+str(tango_pose_adf_device.header.stamp.nsecs)+ ','
        +str(tango_pose_adf_device.translation[0])+ ','+ str(tango_pose_adf_device.translation[1])+ ','+ str(tango_pose_adf_device.translation[2])+ ','
        +str(tango_pose_adf_device.orientation[0])+','+str(tango_pose_adf_device.orientation[1])+','+str(tango_pose_adf_device.orientation[2])+','+str(tango_pose_adf_device.orientation[3])+','
        +str(tango_counter)+'\n') 


     vicon_adf_file.write(str(tango_pose_adf_device.status_code.status)+','+ str(vicon_pose.header.stamp.secs)+ ','+ str(vicon_pose.header.stamp.nsecs)+ ','
       +str(vicon_pose.transform.translation.x)+ ','+str(vicon_pose.transform.translation.y)+ ','+str(vicon_pose.transform.translation.z)+ ','
        +str(vicon_pose.transform.rotation.x)+ ','+str(vicon_pose.transform.rotation.y)+ ','+str(vicon_pose.transform.rotation.z)+ ','+str(vicon_pose.transform.rotation.w)+ ','
        +str(vicon_counter)+'\n')  

     tango_counter +=1;
     vicon_counter +=1;    
    
     vicon_adf_file.close();   
     tango_adf_file.close();
         
def sync_start_vicon_beagle_callback(tango_pose_start_device,beagle_fsr):
     
         global tango_counter;
         global vicon_counter;
         

         
         print ' Relocalized...synced and saving start and adf -- Subject Name',subjectName;
         
           

def listener():
    global mydir;
    global subjectName;
    
    if len(sys.argv) == 1 and mustAnnotate == True:
     print "No Subject chosen... Enter subject below"
     subjectName = raw_input('Enter your Subject name: ')
    else:     
      subjectName = sys.argv[1]
      print 'Subject Name',subjectName;
      
    mydir=mydir+'-'+subjectName;
    
   
    try:
        os.makedirs(mydir)
    except OSError, e:
        if e.errno != 17:
            raise 

    rospy.init_node('listener', anonymous=True)

#    tfBuffer = tf2_ros.Buffer()
#    listener = tf2_ros.TransformListener(tfBuffer)
#    
#    while not rospy.is_shutdown():
#        try:
#            trans = tfBuffer.lookup_transform('device', 'start_of_service', rospy.Time(0))
#        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
#            rate.sleep()
#            continue
        

     # message filter subsribers 
    # @todo tf based message filter
    tango_sub_start= message_filters.Subscriber(tango_topic, TransformStamped) #start to device 
    #vicon_sub= message_filters.Subscriber(vicon_pose_topic,TransformStamped )  # Vicon pose est 
    beagle_sub= message_filters.Subscriber(beagle_topic,FsrDataMsg )


    #message filter sync params
    ts_ = message_filters.ApproximateTimeSynchronizer([tango_sub_start,beagle_sub], 5,20)


    #message filter callbacks 
    ts_.registerCallback(sync_start_vicon_beagle_callback)

    rospy.loginfo("listening to Start and Vicon");
    rospy.spin()
    
    
if __name__ == '__main__':
    listener()
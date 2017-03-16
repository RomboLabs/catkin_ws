#!/usr/bin/env python  
import rospy

import tf2_ros


source_frame ="start_of_service"
child_frame_id ="device"


if __name__ == '__main__':
    rospy.init_node('tf2_listener')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

   # rospy.wait_for_service('spawn')
    #spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    #turtle_name = rospy.get_param('turtle', 'turtle2')
    #spawner(4, 2, 0, turtle_name)

    #turtle_vel = rospy.Publisher('%s/cmd_vel' % turtle_name, geometry_msgs.msg.Twist, queue_size=1)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform('device', 'start_of_service', rospy.Time(0))
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

        print ("trans.transform.translation.x,trans.transform.translation.y",(trans.transform.translation.y, trans.transform.translation.x))
        rate.sleep()
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import numpy as np
import cv2

GObject.threads_init()
Gst.init(None)

def YUV_stream2RGB_frame(data):

    w=640
    h=368
    size=w*h

    stream=np.fromstring(data,np.uint8)


    y=stream[0:size].reshape(h,w)

    u=stream[size:(size+(size/4))].reshape((h/2),(w/2))

    u_upsize=cv2.pyrUp(u)


    v=stream[(size+(size/4)):].reshape((h/2),(w/2))
    v_upsize=cv2.pyrUp(v)

    yuv=cv2.merge((y,u_upsize,v_upsize))

    rgb=cv2.cvtColor(yuv,cv2.cv.CV_YCrCb2RGB)

    cv2.imshow("show",rgb)
    cv2.waitKey(5)

def on_new_buffer(appsink):

   sample = appsink.emit('pull-sample')
   buf=sample.get_buffer()
   data=buf.extract_dup(0,buf.get_size())
   YUV_stream2RGB_frame(data)
   return False

def Init():

   CLI="rtsp://192.168.10.33:554/live.sdp"

   pipline=Gst.parse_launch(CLI)
   appsink=pipline.get_by_name("sink")

   appsink.set_property("max-buffers",20)
   appsink.set_property('emit-signals',True)
   appsink.set_property('sync',False)

   appsink.connect('new-sample', on_new_buffer)

def run():
    pipline.set_state(Gst.State.PLAYING)
    GObject.MainLoop.run()


Init()
run()
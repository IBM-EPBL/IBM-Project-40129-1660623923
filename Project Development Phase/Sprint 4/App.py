from flask import Flask,render_template,Response,request
import cvlib as cv
from cvlib.object_detection import draw_bbox
from PIL import Image
import cv2
import numpy as np
import base64
import time
   
app =Flask(__name__)

def drownDetection(img):
    isDrowning=False
    nimg = np.array(img)
    imgMat=cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)
    bbox, label, conf = cv.detect_common_objects(imgMat)
    print(bbox)
    bbox0=[]
    if (len(bbox) > 0):
        bbox0 = bbox[0] 
        centre = [(bbox0[0] + bbox0[2]) / 2, (bbox0[1] + bbox0[3]) / 2]
        centre0=[]
        if(len(centre0)==0):centre0=np.zeros(2)
        # make vertical and horizontal movement variable
        
        hmov = abs(centre[0] - centre0[0])
        vmov = abs(centre[1] - centre0[1])
        x = time.time()
        t0=time.time()
        threshold = 10
        if (hmov > threshold or vmov > threshold):
            print(x - t0, 's')
            t0 = time.time()
            isDrowning = False
        else:
            print(x - t0, 's')
            if ((time.time() - t0) > 10):
                isDrowning = True        
        print('Is he drowning: ', isDrowning)
        centre0=centre


@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='GET':
        return render_template('index.html')
    if request.method=='POST':
        isDrowning=False
        if(request.data!=None or request.data.isEmpty()):
            img=Image.frombytes("L", (10, 10),base64.b64decode(request.data))  
            drownDetection(img)
            
        return render_template('index.html',data=isDrowning)

if __name__=="__main__":
    app.run(debug=True)

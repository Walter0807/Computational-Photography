import numpy as np 
import cv2 
import glob 
import os
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt

filepath = '5_objects'

for obj in os.listdir(filepath):
    if obj.startswith('.'):
        continue
    objpath = filepath + '/' + obj
    f = open('%s/lights.txt' % objpath, "r")
    content = f.read(); 
    data = np.fromstring(content, dtype=float, sep=' ')
    Lt = data[1:].reshape(int(data[0]),-1)
    # Read images 
    Mt = [] 
    for fname in sorted(glob.glob('%s/*.png' % objpath)):
        if 'mask' in fname:
            mask = cv2.imread(fname, 0)
            mask = np.clip(mask,0.0,1.0)
            mask = mask.reshape(mask.shape[0],mask.shape[1],-1)
            continue
        im = cv2.imread(fname, 0) 
        height, width = im.shape
        Mt.append(im.reshape(-1))
    Mt = np.array(Mt)
    # Photometric stereo computation (least-squares)
    N = np.linalg.lstsq(Lt, Mt)[0].T
    N = normalize(N, axis=1) # normalize to account for diffuse reflectance
    N = np.reshape(N, (height, width, 3)) # Reshape to image coordinates 
    N = (N[:,:,::-1] + 1.0) / 2.0 
    N = (N*mask + 1.0) * 128.0
    cv2.imwrite('results/%s/test_%s.jpg' % (filepath, obj), N)
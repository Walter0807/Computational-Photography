import numpy as np 
import cv2 
import math 
import os
import glob
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
import scipy.io as sio

import warnings
warnings.filterwarnings("ignore")

filepath = 'DiLiGenT/pmsData'

for obj in os.listdir(filepath):
    if obj.startswith('.'):
        continue
    objpath = filepath + '/' + obj
    Lt = np.loadtxt('%s/light_directions.txt' % objpath)
    # Read images 
    Mt = [] 
    for fname in sorted(glob.glob('%s/*.png' % objpath)):
        if 'mask' in fname:
            mask = cv2.imread(fname, 0)
            mask = np.clip(mask,0.0,1.0)
            mask = mask.reshape(mask.shape[0],mask.shape[1],-1)
            continue
        if 'gt' in fname:
            continue
        im = cv2.imread(fname, 0) 
        height, width = im.shape
        Mt.append(im.reshape(-1))
    Mt = np.array(Mt)
    # Photometric stereo computation (least-squares)
    N = np.linalg.lstsq(Lt, Mt)[0].T # M = NL <-> M^T = L^T N^T.
    N = normalize(N, axis=1) # normalize to account for diffuse reflectance
    N = np.reshape(N, (height, width, 3)) # Reshape to image coordinates 
    img = (N[:,:,::-1] + 1.0) / 2.0 
    img = (img*mask + 1.0) * 128.0
    cv2.imwrite('results/DiLiGenT/test_%s.jpg' % (obj), img)
    gt_fname = '%s/Normal_gt.mat' % objpath
    gt = sio.loadmat(gt_fname)['Normal_gt']
    s = np.arccos(np.einsum('ijk, ijk->ij', N, gt))*180/math.pi
    mask = np.squeeze(mask)
    err = np.sum(s*mask) / np.sum(mask)
    print('Case %s, Err=%.5f'%(obj,err))
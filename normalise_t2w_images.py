import os
from os import listdir
from os.path import isfile, join
import matplotlib
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np

loading_path = '/path/to/dhcp_fetal_scans_directory'
saving_path = '/path/to/output_directory_for_normalised_scans'
onlyfiles = [f for f in listdir(loading_path) if isfile(join(loading_path,f))]
for x in onlyfiles:
    full_filename = os.path.join(loading_path, x)
    print('reading', full_filename)
    img = nib.load(full_filename)
    img_shape = img.shape
    print(img_shape)
    img_data = img.get_fdata()
    if len(img_shape) > 3:
        img_data = img_data[:, :, :, 0] #ensures it is not 4D
    new_header = img.header.copy()
    mean_pixel = np.mean(img_data)
    std_pixel = np.std(img_data)
    img_data = (img_data - mean_pixel)/std_pixel
    new_img = nib.nifti1.Nifti1Image(img_data, None, header=new_header)
    new_img_shape = new_img.shape
    print (new_img_shape)
    nib.save(new_img, join(saving_path,x))

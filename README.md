# The dHCP fetal segmentation framework



### **Introduction**


Here, we contribute an age-agnostic software framework based
on deep neural networks for fast and sensitive tissue 
segmentation of fetal brain MRI. 

Our framework was developed, refined,
and evaluated on 249 T2w fetal scans acquired at gestational ages 21 – 38 weeks. Data used to develop the framework was obtained from the **developing human connectome project** 
(dHCP) cohort (http://www.developingconnectome.org/). 


The framework takes volumetric MRI scans of fetal brains (NIFTI files) as input, 
and returns tissue segmentation maps of the following classes as output:
1. Brainstem.
2. CSF.
3. Deep grey matter.
4. Germinal matrix.
5. Cortical grey matter.
6. Outlier tissues.
7. Ventricles.
8. White matter.

.. as well as zero-pixel background regions.


There are two core components to 
our framework:

**a brain detection network:** detects regions of the MRI scan that do not correspond to zero-pixel background or outlier 
tissue class. Output of the brain detection network is then used as a region-of-interest (ROI) mask for the subsequent segmentation network.

**a tissue segmentation network:** segments regions in the MRI scan into one of the aforementioned brain tissue classes.
The network was developed via a human-in-the-loop approach, where an expert fetal image research annotator at 
St. Thomas' Hospital refined the performance of the network, thereby make it more sensitive and robust to different tissue classes. 




### Using the framework


**Setting up DeepMedic:**

Our framework was developed using DeepMedic; an open-source project that offers easy access to deep learning for segmentation of structures of interest in 3D biomedical scans.
DeepMedic needs to be installed for our deep neural networks to be used. Details on how to install and use DeepMedic can be found on 
the project's GitHub (https://github.com/deepmedic/deepmedic); the networks were developed and refined using **v0.7.0**.

**Using the brain detection network:** 

For this step, you will need:
- the model configuration file (bdn_model_config.cfg).
- the network check-point file (bdn.model.ckpt).

You'll also need 
- the test configuration file (bdn_test_config.cfg), which essentially defines how to run the network on the 3D scans of interest.
- the list of 3D scans you need to segment (test_t2w.cfg), you will need to edit this list.
- the list of output file names (bdn_out_names.cfg), each entry here should correspond to a line in the list of scans. You will need to edit this list. 

**Using the tissue segmentation network:** 

Similar to the previous step, you will need:
- the model configuration file (tsn_model_config.cfg).
- the network check-point file (tsn.model.ckpt).
- the test configuration file (tsn_test_config.cfg), 
- the list of 3D scans you need to segment (test_t2w.cfg). Again, you will need to edit this list.
- the list of output file names (bdn_out_names.cfg). Again, each entry here should correspond to a line in the list of scans; you will need to edit this list. 

You'll also need 
- the ROI mask configuration file (roi.cfg). This is a list of brain masks within which tissue segmentation will be carried out. This should be the segmentation
output from the previous step, which can found in the 'predictions' directory. 





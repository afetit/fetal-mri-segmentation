# The DHCP fetal segmentation system

![](https://github.com/afetit/dhcp-fetal-segmentation-tool/blob/master/documentation/for-github-2.png)

---
### **Introduction**

Here, we contribute an automated system based on deep neural networks for fast and sensitive tissue 
segmentation of fetal brain MRI. Our system was developed, refined, and evaluated on 249 fetal scans acquired at gestational ages 21 – 38 weeks. Data used to develop the system was obtained from the **Developing Human Connectome Project (DHCP)** (http://www.developingconnectome.org/), which aims to make major scientific progress by creating the first 4-dimensional connectome of the developing brain.


Currently, the system takes volumetric T2-weighted MRI (NIfTI files) as input, 
and returns back tissue segmentation maps for cortical grey matter. There are two core components to 
our system:

A **brain detection network (BDN)** that detects regions of the scan that do not correspond to zero-pixel background or outlier 
tissues. Output of the BDN can then be used as a region-of-interest (ROI) mask for the subsequent segmentation network.

A **tissue segmentation network (TSN)** that carries out automated image segmentation of cortical grey matter. The TSN was developed via a human-in-the-loop approach, where an expert fetal neuroimage annotator at St Thomas' Hospital helped refine the performance of a network originally trained on automatically generated labels. This allowed us to accelerate the deep learning process for the complex task of fetal neuroimage segmentation with minimal manual labels (fewer than MRI 300 slices). 

---
### Running the system manually


**(a) Set up DeepMedic:**

Our system was developed using DeepMedic; an open-source project that offers easy access to deep learning for segmentation of structures of interest in 3D biomedical scans.
DeepMedic needs to be installed for our networks to be used. Details on how to install and use DeepMedic can be found on 
the project's GitHub (https://github.com/deepmedic/deepmedic), note that the networks were developed and refined using **v0.7.0** of the project. Before moving on to the steps detailed below, we suggest that you familiarise yourself with DeepMedic and the tinyCNN example on the project's GitHub. The project has excellent, clear documentation. 

**(b) Download the segmentation files:**

In essence, our system is a collection of network checkpoints and configuration files that were developed and refined on DHCP fetal scans using DeepMedic. Once you have familiarised yourself with DeepMedic, how to use its command-line syntax, and how its configuration files work, download the directory named *fetal-segmentation-system*; this contains all necessary files to run our system, in addition to example dHCP data to demonstrate the neural networks' utility. Place *fetal-segmentation-system* under the *DeepMedic* directory.

**(c) Run the brain detection network (BDN):** 

This step is where you apply the pre-trained BDN model on the T2-weighted fetal scans you wish to segment. This step only generates brain masks, but you will need those before you carry out tissue segmentation. 

In order to generate the brain masks you will need:
- The BDN model configuration file (bdn_model_config.cfg). This file specifies the architecture of the neural network.
- The BDN network check-point files (bdn.model.ckpt.index and bdn.model.ckpt.data). These hold the final state of the neural network after it has been trained and validated. 
- The test configuration file (bdn_test_config.cfg). This file defines how to run the network on the scans of interest, e.g. where to find the list of scans that we're applying the network on.
- The list of scans you wish to segment (test_t2w.cfg). You will need to edit this list so that each entry points to the path of an individual scan.
- A list that defines how you wish to name output files (bdn_out_names.cfg). Each entry in this file should correspond to an entry in the list of scans file. You will need to edit this list. 

To run the BDN, simply use standard DeepMedic commands as follows. GPU acceleration is recommended and can be specified using the -dev key. 
```
./deepMedicRun -model ./fetal-segmentation-system/bdn/architecture/bdn_model_config.cfg 
               -test ./fetal-segmentation-system/bdn/test/bdn_test_config.cfg 
               -load  ./fetal-segmentation-system/bdn/checkpoint/bdn.model.ckpt
               -dev cuda0
```

**(d) Run the tissue segmentation network (TSN):** 

Once you have generated brain masks for each of the scans you wish to segment, you can now apply the pre-trained TSN model on the scans, while indicating that the generated brain masks need to be used for defining regions-of-interest.  

Similar to the previous step, you will need:
- The TSN model configuration file (tsn_model_config.cfg).
- The TSN network check-point files (tsn.model.ckpt.index and tsn.model.ckpt.data).
- The test configuration file (tsn_test_config.cfg), 
- The list of 3D scans you need to segment (test_t2w.cfg). Again, you will need to edit this list.
- The list of output file names (tsn_out_names.cfg). Again, each entry here should correspond to a line in the list of scans; you will need to edit this list. 

You'll also need 
- The ROI mask configuration file (roi.cfg). This needs to list down the paths to the final segmentation
output from the previous step, which can found in the 'predictions' directory. Each entry in this list should have a corresponding T2-weighted file in the test_t2w.cfg file.

Running the TSN is also straightforward.

```
./deepMedicRun -model ./fetal-segmentation-system/tsn/architecture/tsn_model_config.cfg 
               -test ./fetal-segmentation-system/tsn/test/tsn_test_config.cfg 
               -load  ./fetal-segmentation-system/tsn/checkpoint/tsn.model.ckpt
               -dev cuda0
```

---
### Running the framework from Docker


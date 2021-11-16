# Overwiev

SCAPIS AIDA is the research environment tool with help to prepare large amount of medical data to train, run and generate annonimized medical images using  Generative Adversarial Networks.<br>
The main solving task:<br>
* Establish a generic and work-efficient console platform to prepare, analyse and generate image data from SCAPIS (and others selected datasets)
* Provide a basic knowledge of medical images and load and process them to train GAN
* The work package includes the source datasets processing which meets the requirenments for use on SCAPIS data and implemnent aftewards the metod in robust engine in SCAPISE AI platform.


#Installing / Getting started

## System 
##Create an Environment 
```
conda create --name SCAPIS_AIDA python=3.6
conda info --envs
conda activate ./SCAPIS_AIDA
```
After activating an environment using its prefix, the prompt will look similar to the following:

Clone project into the folder

Prerequisites
```
pip install -r requirements.txt
```

numpy~=1.19.5
opencv-python~=4.5.4.58
matplotlib~=3.3.4
pydicom~=2.2.2
pandas~=1.1.5
tensorflow~=1.15.0
tensorflow-gpu~=1.15.0
scipy~=1.1.0
six~=1.16.0
pillow~=8.4.0

##Requirenments 

[]

##DataSet structure

[]

![](img/BlankDiagram.png)

#Dicom images
Normally DICOM format uses to keeping medical datasets 

#User Gui

CSV dataset files with a labeled slices were loaded onto a dashboardand the framwork  automatically implemented supervised learning and developed optimized classifier with hyperparameters.•


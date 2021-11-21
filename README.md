
###Disclaimer
>This is an internal manual:<br>
> all content, imagery, requirenments and user interface given may be misleading, incomplete, or might change.

# Overwiev
This is a research environment tool which is simplified user-level for prepare large amount of medical data to train, run and generate annonimized medical images using well known
[Generative Adversarial Networks](https://github.com/tkarras/progressive_growing_of_gans). <br>
It is implemented ib **Python** and has a operating system independent layer that allows it to run, potentially, on any OS.<br>
**The main solving tasks:**<br>
* Establish a generic and efficient console platform with possibility to run in Linux terminal to prepare, analyse and generate image data from SCAPIS (and others selected datasets);<br>
* Provide a basic knowledge of medical images, load convert and process them to train anonymized images;<br>
* The work package includes the source datasets processing which meets the requirenments for use on SCAPIS data and implemnent aftewards the metod in robust engine in SCAPISE AI platform.<br>

## **Table of Contents**
2. [Introduction](doc/data.md)<br>
3. [Requirements](doc/requirements.md)<br>
4. [Example of running](doc/data.md)<br>
5. [Analysing of results](doc/data.md)<br>


#Installing / Getting started

## System requirements
- Both Linux and Windows are supported. The latest version is tested under Windows 10. But strongly recommended use OS with max CUDA<=10.1 for compatibility reasons.
It depends on the TensorFlow version used by the authors of PCGAN.
- Python 3.6 (64 bits) installation. To configure environment We recommend Conda.
Additional Python packages listed in the requirements.txt located in the project folder<br>.
##Create an Environment 
```
conda create --name SCAPIS_AIDA python=3.6
conda info --envs
conda activate ./SCAPIS_AIDA
```
Clone project into the folder

###Prerequisites
```
pip install -r requirements.txt
```
>numpy~=1.19.5<br>
opencv-python~=4.5.4.58<br>
matplotlib~=3.3.4<br>
pydicom~=2.2.2<br>
pandas~=1.1.5<br>
tensorflow~=1.15.0<br>
tensorflow-gpu~=1.15.0<br>
scipy~=1.1.0<br>
six~=1.16.0<br>
pillow~=8.4.0<br>

##Requirenments 

[]

##DataSet structure



![](img/BlankDiagram.png)

#Dicom images
Normally DICOM format uses to keeping medical datasets 

#User Gui

To run the programme tipe the following command:
```
python main.py -data_dir "D:/Scapis/SCAPIS_Processed_Data"
```
The `data_dir` argument is required. This is a full  

----------------------------------------
	[0]	Download DCOM images from [drli,ctpa,scapis] into the Dictionary and create JSON:
	[1]	Save Dictionary into Numpy and CSV:
	[2]	Load Dictionary from Numpy and CSV:
	[3]	Plot random Slices:
	[4]	Show slices Info:
	[5]	Hounsfield Units (HU):
	[6]	OpenGL show in 3D:
	[7]	Generate Images by PCGAN:
	[8]	Exit:
----------------------------------------
	Choose your option: 
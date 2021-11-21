## System requirements
- Both Linux and Windows are supported. The latest version is tested under Windows 10. But strongly recommended use OS with max CUDA<=10.1 for compatibility reasons.
It depends on the TensorFlow version used by the authors of PCGAN.
- Python 3.6 (64 bits) installation. To configure environment We recommend Conda.<br>
Additional Python packages listed in the **requirements.txt** located in the project folder<br>.
### Create a new environment 
The environment variable are set globally inside the project's folder, to avoid installing unnecessary packages on the system, then activate it and install the necessary dependencies.
```
conda create --name SCAPIS_AIDA python=3.6
conda info --envs
conda activate ./SCAPIS_AIDA
```
### Prerequisites
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
### Note
At the first start, there may be a message about the need to install additional libraries.<br>
It can be when pixel array data from dicom are decoded from JPEG uncompressed data. And it depends from the supported version of transfer syntaxes by the given packages in the datasets. 
To check which packages needs to be installed additionally, see the list of [Supported Transfer Syntaxes](https://pydicom.github.io/pydicom/stable/old/image_data_handlers.html#guide-compressed).

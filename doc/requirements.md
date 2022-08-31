# System requirements

- Both Linux and Windows are supported. The latest version is tested under Ubuntu 22:</br>

```bash
Distributor ID : Ubuntu
Description    : Ubuntu 22.04.1 LTS
Release        : 22.04
Codename       : jammy
```

-But recommended use OS with max CUDA=11.1 for compatibility reasons.</br>
It depends on the **torch** version used by the authors of StyleGan3.
-Python 3.9 (64 bits) installation. To configure environment we recommend Conda.</br>
Additional Python packages listed in the **environments.yml** located in the project folder.</br>

## Create a new environment

The environment variable are set globally inside the project's folder, to avoid installing unnecessary packages on the system. Then activate it and install the necessary dependencies.

```bash
conda create -f environment.yml
conda info --envs
conda activate SCAPIS_AIDA
```

### Note 0

At the first start, there may be a message about the need to install additional libraries.</br>
It can be when **pixel array** data from dicom are decoded from JPEG uncompressed data. And it depends from the supported version of transfer syntaxes by the given packages in the datasets.
To check which packages needs to be installed additionally, see the list of [Supported Transfer Syntaxes](https://pydicom.github.io/pydicom/stable/old/image_data_handlers.html#guide-compressed).

### Note 1

The TransferSyntaxUID for CTPA data is **1.2.840.10008.1.2.4.90**.

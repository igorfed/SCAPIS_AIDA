# Copyright (c) 2021, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Generate images using pretrained network pickle."""

import os
import re
from typing import List, Optional, Tuple, Union
import matplotlib
import matplotlib.pyplot as plt
import click
import dnnlib
import numpy as np
import PIL.Image
import torch

import legacy
import sys 


import os

import numpy as np
import pydicom
import datetime
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import UID
import SimpleITK as sitk 


def write_dicom(pixel_array, filename, itemnumber, PhotometricInterpretation = 'MONOCHROME2'):
    # Create some temporary filenames
    def time_get():
        dt = datetime.datetime.now()
        time = dt.strftime('%Y%m%d')
        timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
        return time
    
    file_meta = FileMetaDataset()

    
    file_meta.FileMetaInformationGroupLength = 224
    file_meta.MediaStorageSOPClassUID = UID('1.2.752.24.10.1.3246021228.1232722830.1394592702.2170053379')
    file_meta.MediaStorageSOPInstanceUID = "Explicit VR Little Endian"
    file_meta.ImplementationClassUID = UID("1.3.6.1.4.1.9590.100.1.3.100.7.1")
    file_meta.ImplementationVersionName = 'PYDICOM-CREATION'
    file_meta.SourceApplicationEntityTitle = 'PYCHARM'    
    
    ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.SpecificCharacterSet = 'ISO_IR 100'
    ds.ImageType = ['ORIGINAL', 'PRIMARY', 'AXIAL', 'CT_SOM5 SEQ']
    ds.SOPClassUID = 'CT Image Storage'
    ds.SOPClassInstanceUID = UID('1.2.752.24.10.1.3246021228.1232722830.1394592702.2170053379')
    ds.StudyDate = time_get()
    ds.SeriesDate = time_get()
    ds.AcquisitionDate = time_get()
    ds.ContentDate = time_get()
    ds.AccessionNumber = str(itemnumber)  #9497992
    ds.Modality = 'CT'
    ds.Manufacturer = 'Linköping University'
    ds.StudyDescription = 'Image Annonimization'

    ds.PatientName = "Anonimyzed"
    ds.PatientID = "123456"
    ds.PatientSex = "F"
    ds.PatientIdentityRemoved = 'Yes'
    ds.BodyPart = "StyleGan3"
    ds.KVP = '120.0'

    ds.SliceThickness = '5.0'
    ds.DataCollectionDiameter = '500.0'
    ds.ReconstructionDiameter = '500.0'


    ds.AcquisitionNumber = itemnumber
    ds.InstanceNumber = itemnumber
    ds.SamplesPerPixel = itemnumber
    ds.PhotometricInterpretation = PhotometricInterpretation

    ds.Rows = 512
    ds.Columns = 512
    
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = ds.BitsAllocated-1

    ds.PixelSpacing = ['0.9765625', '0.9765625']
    ds.PixelRepresentation = 0
    ds.SmallestImagePixelValue =pixel_array.min()
    ds.LargestImagePixelValue = pixel_array.max()
    ds.WindowCenter = ['40', '40']
    ds.WindowWidth = ['400', '150']
    ds.RescaleSlope = '1.0'
    ds.RescaleType = 'HU'
    ds.ItemNumber = itemnumber
    ds.SliceLocation = 0
    ds.InstanceNumber = itemnumber
    
    pixel_array = pixel_array.astype(np.uint8)
    ds.PixelData = pixel_array.tostring()
    ds.save_as(filename)

    return filename
#----------------------------------------------------------------------------

def parse_range(s: Union[str, List]) -> List[int]:
    '''Parse a comma separated list of numbers or ranges and return a list of ints.

    Example: '1,2,5-10' returns [1, 2, 5, 6, 7]
    '''
    if isinstance(s, list): return s
    ranges = []
    range_re = re.compile(r'^(\d+)-(\d+)$')
    for p in s.split(','):
        m = range_re.match(p)
        if m:
            ranges.extend(range(int(m.group(1)), int(m.group(2))+1))
        else:
            ranges.append(int(p))
    return ranges

#----------------------------------------------------------------------------

def parse_vec2(s: Union[str, Tuple[float, float]]) -> Tuple[float, float]:
    '''Parse a floating point 2-vector of syntax 'a,b'.

    Example:
        '0,1' returns (0,1)
    '''
    if isinstance(s, tuple): return s
    parts = s.split(',')
    if len(parts) == 2:
        return (float(parts[0]), float(parts[1]))
    raise ValueError(f'cannot parse 2-vector {s}')

#----------------------------------------------------------------------------

def make_transform(translate: Tuple[float,float], angle: float):
    m = np.eye(3)
    s = np.sin(angle/360.0*np.pi*2)
    c = np.cos(angle/360.0*np.pi*2)
    m[0][0] = c
    m[0][1] = s
    m[0][2] = translate[0]
    m[1][0] = -s
    m[1][1] = c
    m[1][2] = translate[1]
    return m

#----------------------------------------------------------------------------

@click.command()
@click.option('--network', 'network_pkl', help='Network pickle filename', required=True)
@click.option('--seeds', type=parse_range, help='List of random seeds (e.g., \'0,1,4-6\')', required=True)
@click.option('--trunc', 'truncation_psi', type=float, help='Truncation psi', default=1, show_default=True)
@click.option('--class', 'class_idx', type=int, help='Class label (unconditional if not specified)')
@click.option('--noise-mode', help='Noise mode', type=click.Choice(['const', 'random', 'none']), default='const', show_default=True)
@click.option('--translate', help='Translate XY-coordinate (e.g. \'0.3,1\')', type=parse_vec2, default='0,0', show_default=True, metavar='VEC2')
@click.option('--rotate', help='Rotation angle in degrees', type=float, default=0, show_default=True, metavar='ANGLE')
@click.option('--outdir', help='Where to save the output images', type=str, required=True, metavar='DIR')
def generate_images(
    network_pkl: str,
    seeds: List[int],
    truncation_psi: float,
    noise_mode: str,
    outdir: str,
    translate: Tuple[float,float],
    rotate: float,
    class_idx: Optional[int]
):
    """Generate images using pretrained network pickle.

    Examples:

    \b
    # Generate an image using pre-trained AFHQv2 model ("Ours" in Figure 1, left).
    python gen_images.py --outdir=out --trunc=1 --seeds=2 \\
        --network=https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-r-afhqv2-512x512.pkl

    \b
    # Generate uncurated images with truncation using the MetFaces-U dataset
    python gen_images.py --outdir=out --trunc=0.7 --seeds=600-605 \\
        --network=https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-t-metfacesu-1024x1024.pkl
    """

    print('Loading networks from "%s"...' % network_pkl)
    device = torch.device('cuda')
    with dnnlib.util.open_url(network_pkl) as f:
        G = legacy.load_network_pkl(f)['G_ema'].to(device) # type: ignore

    os.makedirs(outdir, exist_ok=True)

    # Labels.
    label = torch.zeros([1, G.c_dim], device=device)
    if G.c_dim != 0:
        if class_idx is None:
            raise click.ClickException('Must specify class label with --class when using a conditional network')
        label[:, class_idx] = 1
    else:
        if class_idx is not None:
            print ('warn: --class=lbl ignored when running on an unconditional network')

    # Generate images.
    itemnumber = 0
    for seed_idx, seed in enumerate(seeds):
        print('Generating image for seed %d (%d/%d) ...' % (seed, seed_idx, len(seeds)))
        z = torch.from_numpy(np.random.RandomState(seed).randn(1, G.z_dim)).to(device)

        # Construct an inverse rotation/translation matrix and pass to the generator.  The
        # generator expects this matrix as an inverse to avoid potentially failing numerical
        # operations in the network.
        if hasattr(G.synthesis, 'input'):
            m = make_transform(translate, rotate)
            m = np.linalg.inv(m)
            G.synthesis.input.transform.copy_(torch.from_numpy(m))

        img = G(z, label, truncation_psi=truncation_psi, noise_mode=noise_mode)
        img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
        filename = f'{outdir}/seed{seed:04d}.dcm'
        
        

        
        
        Img = PIL.Image.fromarray(img[0].cpu().numpy()) #, 'RGB'
        I = img[0].cpu().numpy()
        I = I[:,:,0]#.astype(np.uint16)
        #print(f'min {np.min(Img)} max {np.max(Img)} {Img.size}{outdir}/seed{seed:04d}.png ')

        inputImageFileName = f'{outdir}/seed{seed:04d}.png'
        Img.save(inputImageFileName)

        #image = np.random.randint(2**16, size=(512, 512), dtype=np.uint16)

        #plt.imshow(I)
        #plt.show()
        #print(type(I), I.shape, type(I[271,231]), I[271,231] )
        #write_dicom(image, filename, itemnumber = itemnumber)
        

        image = sitk.ReadImage(inputImageFileName)
        outputImageFileName = f'{outdir}/seed{seed:04d}.dcm'
        sitk.WriteImage(image, outputImageFileName)


        itemnumber = itemnumber +1
        


#----------------------------------------------------------------------------

if __name__ == "__main__":
    generate_images() # pylint: disable=no-value-for-parameter

#----------------------------------------------------------------------------

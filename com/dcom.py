from com.color import COLOR
import numpy as np
import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset

class DCM:
    # DICOM File Meta Information

    META = b"\x00\x02"
    GROUP_LENGTH_INF = b"\x00\x00"  # Number of bytes following this File Meta Element (end of the Value field) up to
    # and including the last File Meta Element of the Group 2 File Meta Information
    META_INF_VERSION = b"\x00\x01"
    META_STORAGE_SOP_CLASS_UID = b"\x00\x02"  # Uniquely identifies the SOP Class associated with the Data Set.
    META_STORAGE_SOP_INST_UID = b"\x00\x03"  # Uniquely identifies the SOP Instance associated with the Data Set
    # placed in the file and following the File Meta Information.
    TRANS_SYNTAX_UID = b"\x00\x10"
    IMPLEMENTATION_CLASS_UID = b"\x00\x12"
    IMPLEMENTATION_VERSION_NAME = b"\x00\x13"
    SOURCE_APP_ENTITY_TITLE = b"\x00\x16"  # ???
    PRIVATE_INF_CREATOR_UID = b"\x01\x00"  # The UID of the creator of the private information
    PRIVATE_INFO = b"\x01\x02"  # Contains Private Information placed in the File Meta Information. Th

    # Standard Operating Procedures
    SOP = b"\x00\x08"

    SPECIFIC_CHARACTER_SET = b"\x00\x05"
    STUDY_DATE = b"\x00\x20"  # Set to Exame date
    STUDY_TIME = b"\x00\x20"  # Set to Exame date
    SERIES_DATE = b"\x00\x21"  # Series date
    SERIES_TIME = b"\x00\x31"  # Series date
    IMAGE_TYPE = b"\x00\x08"  # Image identification characteristics.
    MODALITY = b"\x00\x60"
    HU = {"Air": -1000,
          "Lung": -500,
          "Fat": -100,
          "Water": 0,
          "CSF": 15,
          "Kidney": 30
          }
    # Study Description Attribute
    # Institution-generated description or classification of the Study (component) performed.
    # Institution-generated description or classification of the Study (component) performed.
    STUDY_DESCRIPTION = b"\x10\x30"
    PATIENT = b"\x00\x10"
    PATIENT_NAME = b"\x00\x10"
    PATIENT_ID = b"\x00\x20"
    PATIENT_SEX = b"\x00\x40"

    PIXEL_DATA_H = b"\x7f\x08"
    PIXEL_DATA_L = b"\x00\x10"


class GROUP:
    META = b"\x00\x02"
    SOP = b"\x00\x08"


class HOU():

    def __init__(self):
        self.xcoords = [-1000, -50, 0, 15, 30, 10, 40, 50, 1000]
        self.xcolors = ["b", "g", "r", "c", "m", "y", "k", "b", "g"]
        self.substance = ["Air", "Fat", "Water", "Fluid", "Kidney", "Muscle", "Blood", "Liver", "Bone"]
        self.num = []
    def ask_user_to_plot_hou(self, slices):
        if slices == []:
            print(COLOR.Red + "Patient list is empty or corrupted" + COLOR.END)
            return
        else:
            user_input = (input(COLOR.Green + "\tChoose specific number of Slice [0,...," + str(len(slices)) + "] or Press ENTER to Random:" + COLOR.END))  # .lower().strip()

            if not user_input: # press Enter
                print("Enter")
                return -1
            elif user_input.isdigit():
                i = int(user_input)
                if (i >= 0 and i<= len(slices)):
                    return i
                else:
                    print(COLOR.Red + '\tInvalid Input' + COLOR.END)
                    #self.ask_user_to_plot_hou(slices)
            else:
                print(COLOR.Red + '\tInvalid Input' + COLOR.END)
                #self.ask_user_to_plot_hou(slices)


    def houndsfield_units(self, slices, dict_CSV, num):
        if slices == []:
            print(COLOR.Red + "Patient list is empty or corrupted" + COLOR.END)
            return
        else:
            print("\tDict:", 'Patients:', slices.ndim, 'Shape:', slices.shape, "Num of Slices:")
            import matplotlib.pyplot as plt
            import random
            if num == -1:
                r = random.randint(0, len(slices))
                s = 'Random Slice' + str(r)

            else:
                r = num
                s = "Houndsfeld Units, Selected Slice:" + str(r)
            fig = plt.figure(s, figsize=(30, 20), dpi=80)
            ax0, ax1 = fig.add_subplot(1, 2, 1), fig.add_subplot(1, 2, 2)
            ax0.imshow(slices[r])
            mean = np.round(np.mean(slices[r]), 3)
            std = np.round(np.std(slices[r]), 3)
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            textstr = '\n'.join((
                r'$Patient= %s$' % (dict_CSV["StudyID"][r],),
                r'$BodyPart= %s$' % (dict_CSV["Body_Part"][r],),
                r'$InstNumber= %d$' % (dict_CSV["Instance_Number"][r],),
                r'$Exposure= %f[mAsec]$' % (dict_CSV["Exposure"][r],),
                r'$Slice= %s$' % (dict_CSV["SliceLocation"][r])))
            ax0.text(0.05, 0.95, textstr, transform=ax0.transAxes, fontsize=8,
                    verticalalignment='top', bbox=props)
            ax0.set_title("Slice:" + str(r), fontsize=10, color='red')
            ax1.set_title("Houndsfeld Units", fontsize=10, color='red')
            y, x, _ = ax1.hist(slices[r].flatten(), bins=1024)
            for xc, xs, xcolor in zip(self.xcoords, self.substance, self.xcolors):
                plt.axvline(x=xc, label='{} : ~{}'.format(xs, xc), c=xcolor)
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            textstr = '\n'.join((
                r'$mean= %s$' % (mean,),
                r'$std= %s$' % (std,),
            ))
            ax1.text(0.05, 0.95, textstr, transform=ax1.transAxes, fontsize=8,
                     verticalalignment='top', bbox=props)

            ax1.grid(which='major', linestyle='-', linewidth='0.5', color='blue')
            ax1.grid(which='minor', linestyle=':', linewidth='0.5', color='green')
            ax1.set_ylabel('Frequency')
            ax1.set_xlabel('Hounsfield Units (HU)')
            ax1.set_yscale('log')

        #plt.hist(data_to_process.flatten(), bins=80, color='c')
        #plt.xlabel("Hounsfield Units (HU)")
        #plt.ylabel("Frequency")
        ax1.legend()
        plt.show()

class DCM_TAG:
    """ This is a class with DICOM TAG constants """

    def __init_(self):
        self.gr = self.GR()
        self.el = self.EL()

    class GR:
        GR0002 = b"\x00\x02"
        GR0004 = b"\x00\x04"
        GR0010 = b"\x00\x10"
        GR0018 = b"\x00\x18"
        GR0020 = b"\x00\x20"

    class EL:
        EL0010 = b"\x00\x02"  # Patient Name
        EL0020 = b"\x00\x20"  # Patient ID
        EL0030 = b"\x00\x30"  # Patient Birth Date
        EL0040 = b"\x00\x40"  # Patient Sex
        EL1010 = b"\x10\x10"  # Patient Age
        EL0032 = b"\x00\x32"  # Image Position


class TAGS:
    # TS = COLOR.Red + "Transfer syntax" + COLOR.END
    StudyID = []
    Patient = []
    Image = []
    Slices = []
    Exposure = []
    Rows = []
    Columns = []
    Pixel_Spacing = []
    Instance_Number = []
    Acquisition_Number = []
    SliceLocation = []
    Body_Part = []
    PatientID = []
    PatientSex = []
    PatientAge = []
    StudyDescription = []
    TransferSyntaxUID = []
    MediaStorageSOPClassUID = []
    MediaStorageSOPInstanceUID = []
    BitsAllocated = []
    BitsStored = []
    HighBit = []
    dict_CSV = {}


TAGS_DICT = {}


class BYTE(DCM):
    @staticmethod
    def byte2concat(high, low):
        return high + low

    @staticmethod
    def byte2Dec(byte):
        return int.from_bytes(byte, byteorder='big', signed=False)


def write_dicom(pixel_array, filename, itemnumber = 0, PhotometricInterpretation = 'MONOCHROME2'):
    # Create some temporary filenames
    from pydicom.dataset import FileDataset, FileMetaDataset
    from pydicom.uid import UID
    def time_get():
        dt = datetime.datetime.now()
        time = dt.strftime('%Y%m%d')
        timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
        return time
    
    #file_meta = FileMetaDataset()
    #file_meta.FileMetaInformationGroupLength = 224
    #file_meta.MediaStorageSOPClassUID = UID('1.2.752.24.10.1.3246021228.1232722830.1394592702.2170053379')
    #file_meta.MediaStorageSOPInstanceUID = "Explicit VR Little Endian"
    #file_meta.ImplementationClassUID = UID("1.3.6.1.4.1.9590.100.1.3.100.7.1")
    #file_meta.ImplementationVersionName = 'PYDICOM-CREATION'
    #file_meta.SourceApplicationEntityTitle = 'PYCHARM'    
    
    #ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)
    #ds.SpecificCharacterSet = 'ISO_IR 100'
    #ds.ImageType = ['ORIGINAL', 'PRIMARY', 'AXIAL', 'CT_SOM5 SEQ']
    #ds.SOPClassUID = 'CT Image Storage'
    #ds.SOPClassInstanceUID = UID('1.2.752.24.10.1.3246021228.1232722830.1394592702.2170053379')
    #ds.StudyDate = time_get()
    #ds.SeriesDate = time_get()
    #ds.AcquisitionDate = time_get()
    #ds.ContentDate = time_get()
    #ds.AccessionNumber = str(itemnumber)  #9497992
    #ds.Modality = 'CT'
    #ds.Manufacturer = 'Linköping University'
    #ds.StudyDescription = 'Image Annonimization'

    #ds.PatientName = "Anonimyzed"
    #ds.PatientID = "123456"
    #ds.PatientSex = "F"
    #ds.PatientIdentityRemoved = 'Yes'
    #ds.BodyPart = "StyleGan3"
    #ds.KVP = '120.0'

    #ds.SliceThickness = '5.0'
    #ds.DataCollectionDiameter = '500.0'
    #ds.ReconstructionDiameter = '500.0'


    #ds.AcquisitionNumber = 1
    #ds.InstanceNumber = 1
    #ds.SamplesPerPixel = 1
    #ds.PhotometricInterpretation = PhotometricInterpretation

    #ds.Rows = 512
    #ds.Columns = 512
    
    #ds.BitsAllocated = 16
    #ds.BitsStored = 16
    #ds.HighBit = ds.BitsStored - 1
    #ds.PixelSpacing = ['0.9765625', '0.9765625']
    #ds.PixelRepresentation = 0
    #ds.SmallestImagePixelValue =0
    #ds.LargestImagePixelValue = 2684
    #ds.WindowCenter = ['40', '40']
    #ds.WindowWidth = ['400', '150']
    #ds.RescaleSlope = '1.0'
    #ds.RescaleType = 'HU'
    #ds.ItemNumber = 0
    #ds.SliceLocation = 0
    #ds.InstanceNumber = 0
    
    if pixel_array.dtype != np.uint16:
        pixel_array = pixel_array.astype(np.uint16)
        ds.PixelData = pixel_array.tostring()
    ds.save_as(filename)

    return filename
"""
  input type：
    .dcm  (folder)      --  sitk/pydicon
    .dcm  (single_img)  --  sitk/pydicom
    .nrrd (sequece_img) --  sitk
    .nii / .nii.gz      --  sitk/nibable
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt  

import SimpleITK as sitk        
import pydicom as dicom
import nibabel as nib

import scipy.ndimage as ndimage  # to reasmple the input image if the spacing of each direction is different 

dcm_folder = 'test_data/folder_name/'
dcm_pth = 'test_data/XXX.dcm'
nrrd_pth = 'test_data/XXX.nrrd'
nii_pth = 'test_data/XXX.nii'

nii_save_pth = ' '
nrrd_save_pth = ' '
dcm_save_pth = ' '

read_mode = 0  
# 0 : sitk: read 3D DCM imgs in a folder
# 1 : sitk: read single 2D DCM imgs 
# 2 : Pydicom: read single 2D DCM imgs
# 3 : nibabel: read single 3D/2D nii imgs
# 4 : sitk: read 4D nrrd sequence img

save_mode = 0  
# 0 : nibable: write to .nii or nii.gz files
# 1 : sitk: wirte to .DCM or .nrrd files

# --------- for 3D DCM images in a folder -------- #
# define a reader and read the serious image
if read_mode == 0:
  reader = sitk.ImageSeriesReader()
  img_names = reader.GetGDCMSeriesFileNames(dcm_folder)
  reader.SetFileNames(img_names)
  image = reader.Execute()
  ds = sitk.GetArrayFromImage(image)                        # warning: the 3D array obtained by SimpleITK with shape [z, y, x]
   
# ---------------- for single image -------------- #
if read_mode == 1:
  single_img = sitk.ReadImage(dcm_pth)
  ds = sitk.GetArrayFromImage(single_img)   # warning: the 3D array obtained by SimpleITK with shape [y, x]

  reader = sitk.ImageFileReader()
  reader.SetFileName(dcm_pth)
  reader.LoadPrivateTagsOn()
  reader.ReadImageInformation()

keys = single_img.GetMetaDataKeys()
  for key in keys:
    print(key, ":", single_img.GetMetaData(key))            # plot the DCM_tags in the current DCM file
        
# --------- for PYdicom  read image -------------- #
if read_mode == 2:
  ds = dicom.read_file(dcm_pth)
  pixel_bytes = ds.PixelData
  pix = ds.pixel_array

# ------- for nii images ------------------------- #
if read_mode == 3:
  ds = nib.load(nii_pth).get_fdata()
  
# ------- for nrrd images (4D) ------------------- #
if read_mode == 4:
  single_img = sitk.ReadImage(nrrd_pth)                     # img with shape=(z y x t)
  spacing_tuple = single_img.GetSpacing()                   # to obtain the spacing of (x y z) warning! the order!
  single_image_array = sitk.GetArrayFromImage(single_img)   # z * y * x * t
  ds_zyxt = single_image_array
  ds_txyz = np.einsum('ijkl->lkji', test_ds_zyxt)           # turn (z y x t) to (t x y z)
  
  ds_0xyz = ds_txyz[0, :, :, :]                             # A certain frame in the sequence (x y z)
  ds = ds_0xyz.copy()
  # resample the img_array to fit (x.spacing, x.spacing, z.spacing)
  resample_test_ds_0xyz = ndimage.zoom(test_ds_0xyz, (1, (spacing_tuple[1]/spacing_tuple[0]), 1), order=3)  

# ----------------------------- save_img ---------------------------- #
# note that before save the processed result, the array should be turn into the img_type, and do not forget give the image the related attributes.
new_array = ds.copy()  # If need to modify the current array, it's up to you. 

# --------------- save img using nibable (nii / nii.gz) ------------- #
if save_mode == 0
  ds_img = nib.load(nii_pth)
  new_img = nib.Nifti1Image(new_nii_array)  
  nib.save(new_img, nii_save_pth)

# --------------- save img using sitk (dcm / nrrd) ---------------- #
if save_mode == 1
  img = sitk.ReadImage(nrrd_pth) 
#   img = sitk.ReadImage(dcm_pth)
  new_img.SetDirection(img.GetDirection())
  new_img.SetOrigin(img.GetOrigin())
  new_img.SetSpacing(img.GetSpacing())
  sitk.WriteImage(new_img, nrrd_save_pth)
#   sitk.WriteImage(new_img, dcm_save_pth)



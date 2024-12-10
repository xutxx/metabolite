from decimal import Decimal
from pyopenms import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#Mass defect window of 50 mDa
def scope(num):
    floor=float(Decimal(num)-Decimal('0.05'))
    upper=float(Decimal(num)+Decimal('0.05'))
    return floor,upper
result=scope('') #input the decimal part of the exact mass of the drug, e.g. 0.3683 for CVB-D

exp = MSExperiment()
MzMLFile().load(".mzML", exp) #Add the file name of the mass spectrometry data in mzML format to be processed
#Selection of quality ranges
mz_start = 0#Please enter the m/z range here.
mz_end = 0#Please enter the m/z range here.
filtered = MSExperiment()
for f in exp:
    if f.getMSLevel()>1:
        filtered.addSpectrum(f)
    if f.getMSLevel() == 1:
        filtered_mz = []
        filtered_int = []
        for mz, i in zip(*f.get_peaks()):
            if mz > mz_start and mz < mz_end:
                filtered_mz.append(mz)
                filtered_int.append(i)
        f.set_peaks((filtered_mz, filtered_int))
        filtered.addSpectrum(f)
#Mass defect filter and nitrogen rule filter
mdf= MSExperiment()
for spec in filtered:
    if spec.getMSLevel()>1:
        mdf.addSpectrum(spec)
    if spec.getMSLevel()==1:
        mdf_mz=[]
        mdf_int=[]
        for mz, i in zip(*spec.get_peaks()):
            arr1, arr2 = np.modf(mz)
            if result[0]<arr1<result[1] and arr2%2!=0: #Even number of N atoms：arr2%2!=0，odd number of N atoms：arr2%2!= 1
                mdf_mz.append(mz)
                mdf_int.append(i)
        spec.set_peaks([mdf_mz,mdf_int])
        mdf.addSpectrum(spec)

tic = MSChromatogram()
tic = mdf.calculateTIC()
mdf.addChromatogram(tic)
MzMLFile().store('.mzML', mdf)#File name of the mass spectrometry data to be saved in mzML format

#mdf-U4HDL 403-50Da+100Da + mdf过滤 + 氮律过滤
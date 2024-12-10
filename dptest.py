from pyopenms import *
import math

standard = OnDiscMSExperiment()
standard.openFile(".mzML")#Reference spectra for comparison
s = standard.getSpectrum(0)
mzs, ints = s.get_peaks()
mzs2=np.around(mzs,decimals=4)#Retain four decimal places
metabolite = OnDiscMSExperiment()
metabolite.openFile(".mzML")#Sample mass spectrum file after processing in the previous module
scan1=[]
for k in range(metabolite.getNrSpectra()):
  spec = metabolite.getSpectrum(k)
  if spec.getMSLevel()==2:
    mzm, intm =spec.get_peaks()
    mzm2=np.around(mzm,decimals=4)
    Ws = (np.power(ints, 0.5)) * (np.power(mzs2, 2))
    Wm = (np.power(intm, 0.5)) * (np.power(mzm2, 2))
    Wd= Ws * Wm
    DP = sum(Wd) / math.sqrt(sum(Ws ** 2) * sum(Wm ** 2))
    if DP>0.8:
      scan1.append(spec.getNativeID()[26:])
exp = MSExperiment()
MzMLFile().load(".mzML", exp)#Input the file that has been processed by the DL.py program here.
DP = MSExperiment()
for spectral in exp:
  if spectral.getNativeID().startswith("function=1") and spectral.getNativeID()[26:] in scan1:
    DP.addSpectrum(spectral)
  if spectral.getNativeID().startswith("function=2") and spectral.getNativeID()[26:] in scan1:
    DP.addSpectrum(spectral)



MzMLFile().store('.mzML', DP)#Save file




from pyopenms import *
import heapq
#Preprocessing: retain the peaks and intensities of the top 50 peaks with the strongest peak intensities in the mass spectrum
od_exp = OnDiscMSExperiment()
od_exp.openFile(".mzML") #Documents saved in the previous module
#remove function=3
e = MSExperiment()
for k in range(od_exp.getNrSpectra()):
  s = od_exp.getSpectrum(k)
  if s.getNativeID().startswith("function=1") or s.getNativeID().startswith("function=2"):
    e.addSpectrum(s)
#Selection of MS2 m/z range
mz_start = 0 #Please enter the m/z range here.
mz_end = 0 ##Please enter the m/z range here.
filtered = MSExperiment()
for sp in e:
  if sp.getMSLevel()==1:
    filtered.addSpectrum(sp)
  if sp.getMSLevel() == 2:
    filtered_mz = []
    filtered_int = []
    for mz, i in zip(*sp.get_peaks()):
      if mz > mz_start and mz < mz_end:
        filtered_mz.append(mz)
        filtered_int.append(i)
    sp.set_peaks((filtered_mz, filtered_int))
    filtered.addSpectrum(sp)
#Introduction of drug standard quality profiles
od_exp = OnDiscMSExperiment()
od_exp.openFile(".mzML") #Drug standard quality profile files
spec=od_exp.getSpectrum() #Drug Standard Quality Chart Index
TOP = MSExperiment()
mz, int = spec.get_peaks()
standard_mz=[]
standard_int=[]
top=heapq.nlargest(50,int)
for i,j in zip(mz,int):
    if j in top:
        standard_mz.append(i)
        standard_int.append(j)
spec.set_peaks((standard_mz, standard_int))
TOP.addSpectrum(spec)
MzMLFile().store('.mzML', TOP) #Preservation of pre-processed standardised mass spectra
#Preprocessing Sample Mass Spectrometry Data
TH50 = MSExperiment()
for spectrum in filtered:
    if spectrum.getMSLevel()==1:
        TH50.addSpectrum(spectrum)
    if spectrum.getMSLevel()==2:
        peak,intensity=spectrum.get_peaks()
        int_top=heapq.nlargest(50,intensity)
        filtered_mz = []
        filtered_int = []
        for x,y in zip(peak,intensity):
            if y in int_top:
                filtered_mz.append(x)
                filtered_int.append(y)
        if len(filtered_int)>50:
            filtered_int=filtered_int[0:50]
        if len(filtered_mz)>50:
            filtered_mz=filtered_mz[0:50]
        spectrum.set_peaks((filtered_mz,filtered_int))
        TH50.addSpectrum(spectrum)
MzMLFile().store('.mzML',TH50) #Save mass spectral data of processed samples





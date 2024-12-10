from pyopenms import *
import pandas as pd
from pyopenms import *
import pandas as pd
import numpy as np
#MS1 retains peaks within 5 ppm of the predicted metabolite parent ion m/z
exp = MSExperiment()
MzMLFile().load(".mzML", exp) #Introduction of post-processing documents from the previous module
metabolite=[] #Input predicted metabolite dataset
match=MSExperiment()
for spec in exp:
    if spec.getMSLevel()>1:
        match.addSpectrum(spec)
    if spec.getMSLevel()==1:
        match_mz=[]
        match_int=[]
        for peak, i in zip(*spec.get_peaks()):
            mz=float('%.4f' % peak)
            for number in metabolite:
                if abs(mz - number) / number * (10 ** 6) <= 5: #5ppm or replace it with 10 ppm.
                    match_mz.append(mz)
                    match_int.append(i)
        spec.set_peaks([match_mz, match_int])
        match.addSpectrum(spec)
MzMLFile().store('.mzML', match) #Save file

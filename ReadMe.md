## Project Introduction

This project realizes automated data processing of high-resolution mass spectrometry data based on Python scripts, which is used to find drug metabolites in complex high-resolution mass spectrometry data. It integrates mass loss filtering algorithm, nitrogen rule filtering algorithm, point integration algorithm, neutral loss filtering algorithm, and metabolite prediction algorithm.

## Environmental Dependencies

Python 3.8

pyopenms library

## Directory structure description

ReadMe.md                 //Help documentation

DL.py                          //Built-in mass loss filter and nitrogen rule filter

preprocessing.py         //Preprocessing algorithm of the built-in point integration algorithm

dptest.py                     //Internal point integration algorithm

match.py                     //Built-in metabolite prediction algorithm

test.mzML                   //Sample data

## Instructions

Before using this project to process high-resolution mass spectrometry data, you need to convert the high-resolution mass spectrometry data from the original format (.raw) to the mzML universal format (.mzML). This step can be achieved through the ProteoWizard 3.0 function of the MSConvert software.

Please install the pyOpenMS library before using this script.

### Data reading and output

MzMLFile().load('.mzML', )

Read the data file code. Please fill in the name of the data file to be processed in quotation marks.

MzMLFile().store('.mzML', )

Output data file code. Please fill in the file name to be saved in quotation marks. The output file format is mzML format.

### About DL.py

Features include mass loss filtering and nitrogen rule filtering

1.  Quality loss filtering

    Line 8, 9 adjust the value '0.05' to change the mass defect window value, here is ±50mDa (common value)

    Line 11 Enter the decimal point of the drug molecule ion in quotation marks

    Line 16, 17 Input m/z range: core structure m/z ± 50Da (common m/z range for mass defect filtering)

2.  Nitrogen rule filtration

    Line 41 When the parent drug has an even number of nitrogen atoms, arr2%2!\=0

    When the parent drug molecular formula contains an odd number of nitrogen atoms, arr2%2!\=1

3.  TIC diagram

    Line 47-49 retains the TIC graph after data processing

### About preprocessing.py

Preprocess the data before point integration 

1.  File input

    Line 5 '.mzML' Input the data name output by the DL.py script (continued from the previous data processing)

    Line 30 Enter the name of the drug standard mass spectrum data file

    Line 31 Input the fragmentation mass spectrum index of the drug standard

2.  File Output

    Line 43 Output reference spectrum (standard fragmentation mass spectrum) for comparison of spectral similarity and calculation of point integral. '.mzML' Input save file name

3.  Data Preprocessing

    Line 3, 4 Enter the m/z range for MS2 spectrum comparison

    Line 36 heapq.nlargest (50, int) is used to filter the top 50 ion peaks (changing the value can change the filtering intensity)

    Line 51 Similarly, filter the ion peaks with the top 50 peak intensities

### About dptest.py

Compare MS2 spectra similarity and calculate point integral

1.  File input

    Line 5 '.mzML' input reference spectrum file name (preprocessing.py Line 43 saves the file)

    Line 10 '.mzML' Input the sample mass spectrometry data file name after preprocessing

2.  Points

    Line 21 sets the DP value to filter the MS2 spectra (the closer the DP value is to 1, the higher the spectral similarity is, and the closer the DP value is to 0, the lower the spectral similarity is)

    Line 24 '.mzML' Input the data name output by the DL.py script (used to retain the corresponding MS1 of the filtered MS2)

### About match.py

Predicting drug metabolites

Line 9 Input the list of predicted metabolite m/z values

Line 20 MS1 molecular ion peak error value within 5ppm (<\= 5 change the value to change the error range)

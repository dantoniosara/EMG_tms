# -*- coding: utf-8 -*-
"""
Created by Sara D'Antonio

The code may be lousy.
Be patient. I am learning.

"""

#%%
import os
import neo 
from neo import Block
from neo.io import Spike2IO, NeoMatlabIO
import matplotlib as plt
from mne.io import concatenate_raws, read_raw_fieldtrip, RawArray,  show_fiff


#%%
cwd = os.getcwd()
print(cwd)

#dir_spike2_files = os.path.join(cwd, 'EMG_files')


neo_subj_1_2ms = neo.io.Spike2IO('subj_1_2ms.smr')

w = NeoMatlabIO(filename='convert_subj_1_2ms.mat')
blocks = neo_subj_1_2ms.read()
w.write(blocks[0])

#%%

# The example here uses the ExampleIO object for creating fake data.
# For actual data and different file formats, consult the NEO documentation.


# Get data from first (and only) segment
seg = neo_subj_1_2ms
title = seg.file_origin

ch_names = list()
data = list()
for ai, asig in enumerate(seg.analogsignals):
    # Since the data does not contain channel names, channel indices are used.
    ch_names.append('Neo %02d' % (ai + 1,))
    # We need the ravel() here because Neo < 0.5 gave 1D, Neo 0.5 gives
    # 2D (but still a single channel).
    data.append(asig.rescale('V').magnitude.ravel())

data = np.array(data, float)

sfreq = int(seg.analogsignals[0].sampling_rate.magnitude)

# By default, the channel types are assumed to be 'misc'.
info = mne.create_info(ch_names=ch_names, sfreq=sfreq)

raw = mne.io.RawArray(data, info)
raw.plot(n_channels=4, scalings={'misc': 1}, title='Data from NEO',
         show=True, block=True, clipping='clamp')
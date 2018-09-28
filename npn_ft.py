''' Plot ft vs Ic of RF NPN Device; compare model to measurement.
__author__ = "Vikram Sekar"
'''

import rfmodeling as mdl
import skrf as rf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re

clr = 'rbg'
ms = 4
fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()

# device name
dutnames = ['dutname',
            'dutname_sim']
sim_string_id = 'sim'

for dutname in dutnames:
    # provide path to data dir of touchstone sp files
    rf.data.pwd = './put_dut_path/'+dutname
    # spot frequency at which fT is calculated
    spotf = 1e9
    # import dc data taken during sparameter measurements
    dcfile = dutname+'_DC.csv'
    df = pd.read_csv(rf.data.pwd + '/' + dcfile)
    # add column for fT/fmax data
    df['FT'] = ""
    # set line / marker styles
    if sim_string_id in dutname:
        sym = '-'
        s_or_m = 'Simu'
    else:
        sym = 'o'
        s_or_m = 'Meas'

    # Read all the rf data in the directory
    npn_data = rf.read_all(rf.data.pwd)
    npn_ns = rf.NetworkSet(npn_data)

    for rfnw in npn_ns:
        dev = mdl.rfnpn(rfnw)
        if sim_string_id in dutname:
            pass
        else:
            dev = dev.d4s()  # Perform 4 step deembedding
        h21 = dev.h21()
        fT = np.absolute(h21[np.where(dev.f == spotf)]) * spotf  # calculate ft

        # extract bias info from dev name. Needs to be modified based on naming scheme.
        vbs = re.findall("VB_\d*\.?\d*", dev.name)
        vbs = re.findall("\d*\.?\d*", str(vbs))
        # find first nonempty string in list
        vb = next(v for v in vbs if v)
        vb = float(vb)

    #    vc = re.findall("VC_\d+\.\d+", dev.name)
        vcs = re.findall("VC_\d*\.?\d*", dev.name)
        vcs = re.findall("\d*\.?\d*", str(vcs))
        # find first nonempty string in list
        vc = next(v for v in vcs if v)
        vc = float(vc)

        # check the bias condition and put in the correct fT value
        df.loc[(df['VB'] == vb) & (df['VC'] == vc), 'FT'] = float(fT)

    unq_vc = df.VC.unique()
    unq_vc = np.sort(unq_vc)
    for vc, c in zip(unq_vc, clr):
        dfv = df.loc[df['VC'] == vc]
        ax.plot(dfv['IC'], dfv['FT']*1e-9, sym+c, ms=ms,
                fillstyle='none', label=s_or_m+': VC='+str(vc)+'V')
        ax2.plot(dfv['VB'], dfv['IC'], sym+c, ms=ms,
                 fillstyle='none', label=s_or_m+': VC='+str(vc)+'V')

    ax.semilogx()
    ax.grid(b=True, which='both', linestyle='--')
    ax.set_ylabel('FT (GHz)')
    ax.set_xlabel('Collector Current (A)')
    ax.set_xlim([1e-6, 1e-1])
    ax.set_ylim([0, 70])
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)

    ax2.semilogy()
    ax2.grid(b=True, which='both', linestyle='--')
    ax2.set_ylabel('IC (A)')
    ax2.set_xlabel('VB (V)')
    ax2.set_xlim([0.7, 1.1])
    ax2.set_ylim([1e-6, 1])
    handles, labels = ax2.get_legend_handles_labels()
    ax2.legend(handles, labels)

ax.set_title(dutnames[0])
ax2.set_title(dutnames[0])
fig.savefig('./dataplots/'+'FTPLOT_'+dutnames[0])
fig2.savefig('./dataplots/'+'ICVB_'+dutnames[0])

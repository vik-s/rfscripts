''' Plot ft vs Ic of RF NPN Device
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
mark_every = None

# device name
dutnames = ['dutname',
            'dutname_sim']

# spot frequencies at which yparameters vs bias is plotted
frlist = ['2GHz', '6GHz', '10GHz', '20GHz']
sim_string_id = 'ext'

for spotf in frlist:
    fig, ax = plt.subplots(figsize=(10, 6))

    for dutname in dutnames:
        # provide path to data dir of touchstone sp files
        rf.data.pwd = './path_to_data/'+dutname

        # import dc data taken during sparameter measurements
        dcfile = dutname+'_DC.csv'
        df = pd.read_csv(rf.data.pwd + '/' + dcfile)
        # add columns for yparameter data
        df['re_y11'] = ""
        df['re_y12'] = ""
        df['re_y21'] = ""
        df['re_y22'] = ""
        df['im_y11'] = ""
        df['im_y12'] = ""
        df['im_y21'] = ""
        df['im_y22'] = ""

        # Read all the rf data in the directory
        npn_data = rf.read_all(rf.data.pwd)
        npn_ns = rf.NetworkSet(npn_data)

        for rfnw in npn_ns:
            d = mdl.rfnpn(rfnw)
            if sim_string_id in dutname:
                sym = '-'
                pass
            else:
                d = d.d4s()   # Perform 4 step deembedding
                sym = 'o'

       #   Extract y parameters at spot frequency
            re_y11 = d.data[spotf].y[:, 0, 0].real
            re_y12 = d.data[spotf].y[:, 0, 1].real
            re_y21 = d.data[spotf].y[:, 1, 0].real
            re_y22 = d.data[spotf].y[:, 1, 1].real
            im_y11 = d.data[spotf].y[:, 0, 0].imag
            im_y12 = d.data[spotf].y[:, 0, 1].imag
            im_y21 = d.data[spotf].y[:, 1, 0].imag
            im_y22 = d.data[spotf].y[:, 1, 1].imag

            # extract bias info from dev name. Needs to be modified based on naming scheme.
            vbs = re.findall("VB_\d*\.?\d*", d.name)
            vbs = re.findall("\d*\.?\d*", str(vbs))
            # find first nonempty string in list
            vb = next(v for v in vbs if v)
            vb = float(vb)

            #vc = re.findall("VC_\d+\.\d+", dev.name)
            vcs = re.findall("VC_\d*\.?\d*", d.name)
            vcs = re.findall("\d*\.?\d*", str(vcs))
            # find first nonempty string in list
            vc = next(v for v in vcs if v)
            vc = float(vc)

            # check the bias condition and put in the correct yp value
            df.loc[(df['VB'] == vb) & (df['VC'] == vc),
                   're_y11'] = float(re_y11)*1e3
            df.loc[(df['VB'] == vb) & (df['VC'] == vc),
                   're_y12'] = float(-re_y12)*1e3
            df.loc[(df['VB'] == vb) & (df['VC'] == vc),
                   're_y21'] = float(re_y21)*1e3
            df.loc[(df['VB'] == vb) & (df['VC'] == vc),
                   're_y22'] = float(re_y22)*1e3
            df.loc[(df['VB'] == vb) & (df['VC'] == vc),
                   'im_y11'] = float(im_y11)*1e3
            df.loc[(df['VB'] == vb) & (df['VC'] == vc),
                   'im_y12'] = float(-im_y12)*1e3
            df.loc[(df['VB'] == vb) & (df['VC'] == vc),
                   'im_y21'] = float(-im_y21)*1e3
            df.loc[(df['VB'] == vb) & (df['VC'] == vc),
                   'im_y22'] = float(im_y22)*1e3

        x_limits = [1e-4, 1e-1]
        y_limits = [1e-3, 1e3]
        unq_vc = df.VC.unique()
        for vc, c in zip(unq_vc, clr):
            dfv = df.loc[df['VC'] == vc]

            plt.subplot(241)
            plt.plot(dfv['IC'], dfv['re_y11'], sym+c, ms=ms,
                     fillstyle='none', markevery=mark_every)
            plt.xscale('log')
            plt.yscale('log')
            plt.grid(b=True, which='both', linestyle='--')
            plt.xlabel('Collector Current (A)')
            plt.xlim(x_limits)
            plt.ylim(y_limits)
            plt.title('Re(y11) [mA/V]', fontsize=10)

            plt.subplot(242)
            plt.plot(dfv['IC'], dfv['re_y12'], sym+c, ms=ms,
                     fillstyle='none', markevery=mark_every)
            plt.xscale('log')
            plt.yscale('log')
            plt.grid(b=True, which='both', linestyle='--')
            plt.xlabel('Collector Current (A)')
            plt.xlim(x_limits)
            plt.ylim(y_limits)
            plt.title('Re(-y12) [mA/V]', fontsize=10)

            plt.subplot(243)
            plt.plot(dfv['IC'], dfv['re_y21'], sym+c, ms=ms,
                     fillstyle='none', markevery=mark_every)
            plt.xscale('log')
            plt.yscale('log')
            plt.grid(b=True, which='both', linestyle='--')
            plt.xlabel('Collector Current (A)')
            plt.xlim(x_limits)
            plt.ylim(y_limits)
            plt.title('Re(y21) [mA/V]', fontsize=10)

            plt.subplot(244)
            plt.plot(dfv['IC'], dfv['re_y22'], sym+c, ms=ms,
                     fillstyle='none', markevery=mark_every)
            plt.xscale('log')
            plt.yscale('log')
            plt.grid(b=True, which='both', linestyle='--')
            plt.xlabel('Collector Current (A)')
            plt.xlim(x_limits)
            plt.ylim(y_limits)
            plt.title('Re(y22) [mA/V]', fontsize=10)

            plt.subplot(245)
            plt.plot(dfv['IC'], dfv['im_y11'], sym+c, ms=ms,
                     fillstyle='none', markevery=mark_every)
            plt.xscale('log')
            plt.yscale('log')
            plt.grid(b=True, which='both', linestyle='--')
            plt.xlabel('Collector Current (A)')
            plt.xlim(x_limits)
            plt.ylim(y_limits)
            plt.title('Im(y11) [mA/V]', fontsize=10)

            plt.subplot(246)
            plt.plot(dfv['IC'], dfv['im_y12'], sym+c, ms=ms,
                     fillstyle='none', markevery=mark_every)
            plt.xscale('log')
            plt.yscale('log')
            plt.grid(b=True, which='both', linestyle='--')
            plt.xlabel('Collector Current (A)')
            plt.xlim(x_limits)
            plt.ylim(y_limits)
            plt.title('Im(-y12) [mA/V]', fontsize=10)

            plt.subplot(247)
            plt.plot(dfv['IC'], dfv['im_y21'], sym+c, ms=ms,
                     fillstyle='none', markevery=mark_every)
            plt.xscale('log')
            plt.yscale('log')
            plt.grid(b=True, which='both', linestyle='--')
            plt.xlabel('Collector Current (A)')
            plt.xlim(x_limits)
            plt.ylim(y_limits)
            plt.title('Im(-y21) [mA/V]', fontsize=10)

            plt.subplot(248)
            plt.plot(dfv['IC'], dfv['im_y22'], sym+c, ms=ms,
                     fillstyle='none', markevery=mark_every)
            plt.xscale('log')
            plt.yscale('log')
            plt.grid(b=True, which='both', linestyle='--')
            plt.xlabel('Collector Current (A)')
            plt.xlim(x_limits)
            plt.ylim(y_limits)
            plt.title('Im(y22) [mA/V]', fontsize=10)

    plt.show()
    plt.tight_layout()
    plt.savefig('./dataplots/'+'Yat'+spotf+'_'+dutnames[0]+'.png')

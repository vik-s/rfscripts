''' Plot unilateral gain and MSG of RF NPN Device
__author__ = "Vikram Sekar"
'''

import rfmodeling as mdl
import skrf as rf
import matplotlib.pyplot as plt

f1 = ['dutname.s2p',
      'dutname_sim.s2p']

sim_string_id = 'sim'
dutname = 'dutname'
clr = 'kk'
ms = 4

plt.figure(1, figsize=(10, 5))

for f, c in zip(f1, clr*2):

    rfnw = rf.Network(f)
    dev = mdl.rfnpn(rfnw)
    if sim_string_id in f:
        sym = '-'
        lbl = 'RC-Ext'
    else:
        # dev = dev.d4s()   # Perform 4 step deembedding
        sym = 'o'
        lbl = 'Meas'

    powergain = dev.gu()
    msg = dev.msg()

    plt.subplot(121)
    plt.plot(dev.f*1e-9, powergain, sym+c, ms=ms, fillstyle='none', label=lbl)
    plt.xscale('log')
    plt.grid(b=True, which='both', linestyle='--')
    plt.ylabel('Unilateral Power Gain (dB)', fontsize=11)
    plt.xlabel('Freq. (GHz)', fontsize=11)
    plt.xlim([0.5, 20])  # plt.ylim([0,0.015])
    plt.legend(loc='best')

    plt.subplot(122)
    plt.plot(dev.f*1e-9, msg, sym+c, ms=ms, fillstyle='none', label=lbl)
    plt.xscale('log')
    plt.grid(b=True, which='both', linestyle='--')
    plt.ylabel('Max. Stable Gain (dB)', fontsize=11)
    plt.xlabel('Freq. (GHz)', fontsize=11)
    plt.xlim([0.5, 20])  # plt.ylim([0,0.015])
    plt.legend(loc='best')
#plt.suptitle(dutname+', Vce=5V, Vbe=0.81V, 0.83V, 0.85V', fontsize=11)
plt.show()
# plt.savefig('./dataplots/'+'Gains_'+dutname+'.png')

''' Plot y-parameters of RF NPN Device
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
ms = 6

plt.figure(1, figsize=(18, 6))

for f, c in zip(f1, clr*2):

    rfnw = rf.Network(f)
    newfreq = rf.Frequency(0.5, 20, 40, 'ghz')
    rfnw = rfnw.interpolate(newfreq)
    dev = mdl.rfnpn(rfnw)
    if sim_string_id in f:
        sym = '-'
        lbl = 'RC-Ext'
    else:
        # dev = dev.d4s(opsh='OpenShortx5.s2p', shop='ShortOpenx5_to20GHz.s2p')   # Perform 4 step deembedding
        sym = 'o'
        lbl = 'Meas'

    plt.subplot(241)
    plt.plot(dev.f*1e-9, dev.data.y[:, 0, 0].real,
             sym+c, ms=ms, fillstyle='none', label=lbl)
    plt.xscale('linear')
    plt.grid(b=True, which='both', linestyle='--')
    plt.ylabel('Real Y11')
    plt.xlabel('Freq. (GHz)')
    plt.xlim([0, 10])
    plt.ylim([0, 0.02])
    plt.legend(loc='best')

    plt.subplot(242)
    plt.plot(dev.f*1e-9, dev.data.y[:, 0, 0].imag,
             sym+c, ms=ms, fillstyle='none', label=lbl)
    plt.xscale('linear')
    plt.grid(b=True, which='both', linestyle='--')
    plt.ylabel('Imag Y11')
    plt.xlabel('Freq. (GHz)')
    plt.xlim([0, 10])
    plt.ylim([0, 0.05])
    plt.legend(loc='best')

    plt.subplot(243)
    plt.plot(dev.f*1e-9, dev.data.y[:, 0, 1].real,
             sym+c, ms=ms, fillstyle='none', label=lbl)
    plt.xscale('linear')
    plt.grid(b=True, which='both', linestyle='--')
    plt.ylabel('Real Y12')
    plt.xlabel('Freq. (GHz)')
    plt.xlim([0, 10])
    plt.ylim([-8e-4, 0])
    plt.legend(loc='best')

    plt.subplot(244)
    plt.plot(dev.f*1e-9, dev.data.y[:, 0, 1].imag,
             sym+c, ms=ms, fillstyle='none', label=lbl)
    plt.xscale('linear')
    plt.grid(b=True, which='both', linestyle='--')
    plt.ylabel('Imag Y12')
    plt.xlabel('Freq. (GHz)')
    plt.xlim([0, 10])
    plt.ylim([-1e-2, 0])
    plt.legend(loc='best')

    plt.subplot(245)
    plt.plot(dev.f*1e-9, dev.data.y[:, 1, 0].real,
             sym+c, ms=ms, fillstyle='none', label=lbl)
    plt.xscale('linear')
    plt.grid(b=True, which='both', linestyle='--')
    plt.ylabel('Real Y21')
    plt.xlabel('Freq. (GHz)')
    plt.xlim([0, 10])
    plt.ylim([0, 0.5])
    plt.legend(loc='best')

    plt.subplot(246)
    plt.plot(dev.f*1e-9, dev.data.y[:, 1, 0].imag,
             sym+c, ms=ms, fillstyle='none', label=lbl)
    plt.xscale('linear')
    plt.grid(b=True, which='both', linestyle='--')
    plt.ylabel('Imag Y21')
    plt.xlabel('Freq. (GHz)')
    plt.xlim([0, 10])
    plt.ylim([-0.3, 0])
    plt.legend(loc='best')

    plt.subplot(247)
    plt.plot(dev.f*1e-9, dev.data.y[:, 1, 1].real,
             sym+c, ms=ms, fillstyle='none', label=lbl)
    plt.xscale('linear')
    plt.grid(b=True, which='both', linestyle='--')
    plt.ylabel('Real Y22')
    plt.xlabel('Freq. (GHz)')
    plt.xlim([0, 10])
    plt.ylim([0, 3e-3])
    plt.legend(loc='best')

    plt.subplot(248)
    plt.plot(dev.f*1e-9, dev.data.y[:, 1, 1].imag,
             sym+c, ms=ms, fillstyle='none', label=lbl)
    plt.xscale('linear')
    plt.grid(b=True, which='both', linestyle='--')
    plt.ylabel('Imag Y22')
    plt.xlabel('Freq. (GHz)')
    plt.xlim([0, 10])
    plt.ylim([0, 3e-2])
    plt.legend(loc='best')

plt.tight_layout()
#plt.suptitle(dutname+', Vce=1.8V, Vbe=0.9V', fontsize=11)
plt.show()
plt.savefig('./dataplots/'+'YvsF_'+dutname+'.png')

"""
Put script documenation here.
"""

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from pymeasure.instruments.rohdeschwarz import RohdeSMB100A, RohdeFSQ
from pymeasure.instruments.agilent import Agilent4156, AgilentU2040X
from pymeasure.log import console_log, file_log

import numpy as np
import pandas as pd


class HarmonicTest(object):
    """
    Class to define all the calibration and measurement sequences to measure harmonics and power handling in RF switch and amplifier devices.
    """

    def __init__(self, sweep_values, **kwargs):
        self.smu = Agilent4156(
            "GPIB0::25", read_termination='\n', write_termination='\n', timeout=None)
        log.info('Connected to {}'.format(self.smu.id))

        self.pm = AgilentU2040X(
            'USB0::0x2A8D::0x1E01::MY56360005::0::INSTR', timeout=None)
        log.info('Connected to {}'.format(self.pm.id))

        self.sig = RohdeSMB100A(
            "GPIB0::29", read_termination='\n', write_termination='\n', timeout=None)
        log.info('Connected to {}'.format(self.sig.id))

        self.sa = RohdeFSQ("GPIB0::20", read_termination='\n',
                           write_termination='\n', timeout=None)
        log.info('Connected to {}'.format(self.sa.id))

        self.DEV_TYPE = 'SWITCH'    # or AMPLIFIER
        self.FUND_FREQ = 983  # MHz
        self.CAL_POWER = -50  # dBm
        self.RES_BW = 100  # Hz
        self.FREQ_SPAN = 1  # kHz
        self.SWP_AVG = 10
        self.SWEEP_VALUES = sweep_values
        self.NHARMONICS = 3

    def setup_instruments(self):
        """ Apply instrument settings """

        # signal generator
        self.sig.reset()
        self.sig.freq_unit = 'MHz'
        self.sig.power_unit = 'DBM'
        self.sig.fixed_freq = self.FUND_FREQ
        self.sig.power_level = self.CAL_POWER
        log.info('Finished setting up signal generator.')

        # signal analyzer
        self.sa.reset()
        self.sa.freq_unit = 'MHz'
        self.sa.power_unit = 'DBM'
        self.sa.center_freq = self.FUND_FREQ
        self.sa.freq_unit = 'kHz'
        self.sa.freq_span = self.FREQ_SPAN
        self.sa.freq_unit = 'Hz'
        self.sa.res_bw = self.RES_BW
        self.sa.video_bw = self.RES_BW
        self.sa.sweep_count = self.SWP_AVG
        self.sa.continuous_mode = 'OFF'
        self.sa.all_markers_off()
        self.sa.freq_counter = 'ON'
        self.freq_unit = 'MHz'
        log.info('Finished setting up signal analyzer.')

        # setup power meter
        self.pm.reset()
        self.pm.freq_unit = 'MHZ'
        self.pm.freq = self.FUND_FREQ
        self.pm.continuous_mode = 'OFF'
        log.info('Finished setting up power meter.')

    def input_calibration(self):
        """ Determine input loss offset via power calibration """
        input(
            'Connect power meter to probe end of the input RF cable. Press any Enter to continue...')
        self.sig.output = 'ON'
        self.sig.power_level = self.CAL_POWER
        self.pm.init()
        self.INPUT_OFFSET = self.pm.read
        self.sig.output = 'OFF'

import numpy as np
from MyVISA.instruments import SpectrumAnalyzer

class SA_RSA5065(SpectrumAnalyzer):
    """ 
    Rigol RSA5065 Spectrum Analyzer
    """

    def __init__(self, res_string: str):
        super().__init__(res_string)

        self.core.query('*ESE?')
        self.core.query('*SRE?')
        self.core.write('*ESE 61')
        self.core.write('*SRE 52')
        self.core.write('STAT:QUES:POW:ENAB 15')
        self.core.write('FORM:TRAC REAL,32')
        self.core.write('INIT:CONT 0')

    def setup_display(self, unit: str | None = None,
                        ref: int | None = None,
                        pdiv: int | None = None):
        if unit is not None:
            self.core.write('UNIT:POW ' + unit)
        if ref is not None:
            self.core.write(f'DISP:WIND:TRAC:Y:RLEV {ref}')
        if pdiv is not None:
            self.core.write(f'DISP:WIND:TRAC:Y:PDIV {pdiv}')
        self._check_registers()

    def setup_meas(self, trac_type: str | None = None,
                        cont: int | None = None,
                        av_num: int | None = None,
                        det: str | None = None,
                        filt: str | None = None,
                        fcent: float | None = None,
                        span: float | None = None,
                        fstart: float | None = None,
                        fstop: float | None = None,
                        rbw: float | None = None,
                        vbw: float | None = None,
                        points: int | None = None,
                        t: float | None = None,
                        att: int | None = None,
                        gain: int | None = None):
        if trac_type is not None:
            self.core.write(f'TRAC1:TYPE {trac_type}')
        if cont is not None:
            if cont in (0, 1):
                self.core.write(f'INIT:CONT {cont}')
        if av_num is not None:
          self.core.write(f'AVER:COUN {av_num}')
        if det is not None:
            self.core.write(f'DET:FUNC {det}')
        if filt is not None:
            self.core.write(f'BWID:{filt}')
        if fcent is not None:
            self.core.write(f'FREQ:CENT {fcent} MHz')
        if span is not None:
            self.core.write(f'FREQ:SPAN {span} MHz')
        if fstart is not None:
            self.core.write(f'FREQ:START {fstart} MHz')
        if fstop is not None:
            self.core.write(f'FREQ:STOP {fstop} MHz')
        if rbw is not None:
            self.core.write(f'BWID:RES {rbw} kHz')
        if vbw is not None:
            self.core.write(f'BWID:VID {vbw} kHz')
        if points is not None:
            self.core.write(f'SWE:POIN {points}')
        if t is not None:
            self.core.write(f'SWE:TIME {t}')
        if gain is not None:
            if gain in (0, 1):
                self.core.write(f'POW:RF:GAIN {gain}')
        if att is not None:
            self.core.write(f'POW:RF:ATT {att}')
        f1 = float(self.core.query('FREQ:START?'))
        f2 = float(self.core.query('FREQ:STOP?'))
        n = float(self.core.query('SWE:POIN?'))
        self._f_ax = (f1, n, f2)
        self._check_registers()

    def initiate(self):
        self._called = False
        self._status = 'Sweeping...'
        self.core.write('INIT:IMM')
        self._check_registers()

    def stop(self):
        self.core.query('*ESR?')
        self._called = True
        self._status = 'Ready'

    def get_data(self) -> tuple:
        try:
            freqs = np.linspace(self._f_ax[0], self._f_ax[2], int(self._f_ax[1]))
            data = self.core.query_binary_values('TRAC? TRACE1', datatype='f', container=np.ndarray)
            self._check_registers()
            return freqs, data, self._called
        except Exception:
            return None, None, self._called

    def save_data(self, filename: str):
        self.core.write('MMEM:STOR:TRAC:DATA TRACE1,' + filename + '.csv')
        self._check_registers()

    def save_screen(self, filename: str):
        self.core.write('MMEM:STOR:SCR ' + filename + '.bmp')
        self._check_registers()

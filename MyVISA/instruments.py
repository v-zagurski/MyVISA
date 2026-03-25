from pyvisa.resources import MessageBasedResource
from MyVISA.instmanager import InstrumentManager

im = InstrumentManager()

def regviewer(value: float) -> list[int]:
    pos_list = []
    pos=0
    while int(value) >= (1<<pos):
      if int(value) & (1<<pos):
        pos_list.append(pos)
      pos=pos+1
    return pos_list

class SpectrumAnalyzer:
    def __init__(self, res_string: str):
        self._str: str = res_string
        self.core: MessageBasedResource = im.open_inst(self._str)
        self.core.timeout = 1000
        self.core.write_termination = '\n'
        self.core.read_termination = '\n'
        self._called: bool = False
        self._status: str = 'Ready'
        self._idn: str = self.core.query('*IDN?')
        self._f_ax: tuple = (None, None, None)
        self._check_registers()

    def _check_registers(self):
        powval = float(self.core.query('STAT:QUES:POW?'))
        if powval != 0:
            self._called = True
            self._status = 'Dangerous input level!'

        operval = float(self.core.query('STAT:OPER:COND?'))
        self._oper = regviewer(operval)

        stbval = float(self.core.query('*STB?'))
        self._stb = regviewer(stbval)
        if 4 in self._stb:
            self._status = 'Message available!'

        esrval = float(self.core.query('*ESR?'))
        self._esr = regviewer(esrval)
        if any(value in [2, 3, 4, 5] for value in self._esr):
            err = self.core.query('SYST:ERR?')
            self._status = f'Error occured! {err}'
        if 0 in self._esr:
            self._called = True
            self._status = 'Ready'

    def close(self):
        im.close_inst(self._str)

class Generator:
    def __init__(self, res_string: str):
        self._str: str = res_string
        self.core: MessageBasedResource = im.open_inst(self._str)
        self.core.timeout = 1000
        self.core.write_termination = '\n'
        self.core.read_termination = '\n'
        self._called: bool = False
        self._status: str = 'Ready'
        self._idn: str = self.core.query('*IDN?')

    def _check_registers(self):
        powval = float(self.core.query('STAT:QUES:POW?'))
        if powval != 0:
            self._called = True
            self._status = 'Dangerous input level!'

        stbval = float(self.core.query('*STB?'))
        self._stb = regviewer(stbval)
        if 4 in self._stb:
            self._status = 'Message available!'

        esrval = float(self.core.query('*ESR?'))
        self._esr = regviewer(esrval)
        if any(value in [2, 3, 4, 5] for value in self._esr):
            err = self.core.query('SYST:ERR?')
            self._status = f'Error occured! {err}'
        if 0 in self._esr:
            self._called = True
            self._status = 'Ready'

    def close(self):
        im.close_inst(self._str)

from MyVISA.instruments import Generator

class G_1465F(Generator):
    """ 
    Ceyear 1465F Signal Generator
    """

    def __init__(self, res_string: str):
        super().__init__(res_string)

        self.core.write("*ESE 61")
        self.core.write('*SRE 48')
        self.core.write('STAT:QUES:POW:ENAB 15')
        self.core.write('FREQ:MODE FIX')
        self.core.write('OUTP 0')

    def setup_output(self, fcent: float | None = None,
                           power: float | None = None,
                           out: bool = False):
        if fcent is not None:
            self.core.write(f'FREQ {fcent} MHz')
        if power is not None:
            self.core.write(f'POW {power} dBm')
        match out:
            case True:
                self.core.write('OUTP 1')
            case False:
                self.core.write('OUTP 0')
        self._check_registers()

    def setup_mod(self, mod_type: str | None = None,
                        shape: str | None = None,
                        freq1: float | None = None,
                        freq2: float | None = None,
                        dep: float | None = None,
                        dev: float | None = None,
                        period: float | None = None,
                        stat: bool = False,
                        out: bool = False):
        if mod_type is not None:
            match mod_type:
                case 'AM':
                    self.core.write('FM:STAT 0')
                    self.core.write('PM:STAT 0')
                    if stat:
                        self.core.write('AM:STAT 1')
                    else:
                        self.core.write('AM:STAT 0')
                    if shape is not None:
                        self.core.write(f'AM:INT:SHAP {shape}')
                        self.core.write(f'AM:INT:FREQ {freq1} Hz')
                    if dep is not None:
                        self.core.write(f'AM:DEPT {dep}')
                    if out:
                        self.core.write('OUTP:MOD 1')
                    else:
                        self.core.write('OUTP:MOD 0')
                case 'FM':
                    if stat:
                        self.core.write('FM:STAT 1')
                    else:
                        self.core.write('FM:STAT 0')
                    self.core.write('PM:STAT 0')
                    self.core.write('AM:STAT 0')
                    if shape is not None:
                        self.core.write(f'FM:INT:SHAP {shape}')
                        if shape == 'SWEP':
                            self.core.write(f'FM:INT:FREQ {freq1} kHz')
                            self.core.write(f'FM:INT:FREQ:ALT {freq2} kHz')
                            self.core.write(f'FM:INT:SWE:TIME {period} ms')
                        else:
                           self.core.write(f'FM:INT:FREQ {freq1} kHz')
                        if dev is not None:
                            self.core.write(f'FM:DEV {dev} kHz')
                        if out:
                            self.core.write('OUTP:MOD 1')
                        else:
                            self.core.write('OUTP:MOD 0')
                case 'PM':
                    self.core.write('FM:STAT 0')
                    if stat:
                        self.core.write('PM:STAT 1')
                    else:
                        self.core.write('PM:STAT 0')
                    self.core.write('AM:STAT 0')
                    if shape is not None:
                        self.core.write(f'PM:INT:SHAP {shape}')
                        if shape == 'SWEP':
                            self.core.write(f'PM:INT:FREQ {freq1} kHz')
                            self.core.write(f'PM:INT:FREQ:ALT {freq2} kHz')
                            self.core.write(f'PM:INT:SWE:TIME {period} ms')
                        else:
                           self.core.write(f'PM:INT:FREQ {freq1} kHz')
                        if dev is not None:
                            self.core.write(f'PM:DEV {dev} rad')
                        if out:
                            self.core.write('OUTP:MOD 1')
                        else:
                            self.core.write('OUTP:MOD 0')
        else:
            if out:
                self.core.write('OUTP:MOD 1')
            else:
                self.core.write('OUTP:MOD 0')
        self._check_registers()

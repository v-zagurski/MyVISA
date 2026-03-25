from MyVISA.SA_4051H import SA_4051H

resource_name = 'TCPIP0::169.254.19.125::5025::SOCKET'

san = SA_4051H(resource_name)
print(san._idn, san._status, sep='\n')

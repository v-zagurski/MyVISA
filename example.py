from MyVISA.SA_4051H import SA_4051H

resource_name = 'TCPIP0::169.254.19.125::5025::SOCKET'

san = SA_4051H(resource_name)
print(san._idn, san._status, sep='\n')

san.setup_meas(trac_type='MAXH',
               cont=0,
               av_num=10,
               det='POS',
               filt='SHAP GAUS',
               fcent=950,
               span=100,
               rbw=100,
               vbw=100,
               points=1000,
               att=10,
               gain=0
               )
san.setup_display(unit='DBM', 
                  ref=0,
                  pdiv=10
                  )
san.initiate()
san.close()
'''
Обработать строку nat таким образом, чтобы в имени интерфейса вместо FastEthernet было GigabitEthernet. 
'''
NAT = "ip nat inside source list ACL interface FastEthernet0/1 overload"
print(NAT.replace('FastEthernet', 'GigabitEthernet'))

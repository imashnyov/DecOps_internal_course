'''
Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде ...
'''
ospf_route = 'O        10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0 \n ,\u2192'

data = ospf_route.replace(',','').split()
print(f'{"Protocol:":<20}{data[0]}\n{"Prefix:":<20}{data[1]}\n{"AD/Metric:":<20}{data[2]}\n{"Next-Hop:":<20}{data[4]} \
\n{"Last update:":<20}{data[5]}\n{"Outbound Interface:":<20}{data[6]} ')


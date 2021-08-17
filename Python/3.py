'''
Получить из строки config список VLAN-ов вида: ['1', '3', '10', '20', '30', '100']
'''
config = 'switchport trunk allowed vlan 1,3,10,20,30,100'
digits_in_config = config.split(' ')[4].split(',')
print(digits_in_config)
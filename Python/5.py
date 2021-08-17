'''
Из строк command1 и command2 получить список VLAN-ов, которые есть и в команде command1 и в команде command2. 
Результатом должен быть список: ['1', '3', '8']
'''
command1 = 'switchport trunk allowed vlan 1,2,3,5,8' 
command2 = 'switchport trunk allowed vlan 1,3,8,9'
digits_in_command1 = command1.split(' ')[4].split(',')
digits_in_command2 = command2.split(' ')[4].split(',')
sum_of_digits = sorted(list(set(digits_in_command1).intersection(set(digits_in_command2))))
print(sum_of_digits)
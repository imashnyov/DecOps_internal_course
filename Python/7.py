'''
Преобразовать MAC-адрес mac в двоичную строку такого вида: 101010101010101010111011101110111100110011001100
'''
mac = 'AAAA:BBBB:CCCC'
a = mac.split(':')
print(f'{int(a[0], 16):b}{int(a[1], 16):b}{int(a[2], 16):b}')
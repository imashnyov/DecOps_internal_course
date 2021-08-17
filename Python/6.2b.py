'''
Сделать копию скрипта задания 6.2a.
Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова. 
'''
ip = input("Input IP-address: ")

while True:
    split_ip = ip.split('.')
    if ip.count('.') == 3 and all(int(i) in range(0,256) for i in split_ip): #check correct ip
        if ip == '255.255.255.255':
            print("local broadcast")
        elif ip == '0.0.0.0':
            print("unassigned")
        elif int(split_ip[0]) in range(1,224):
            print("unicast")
        elif int(split_ip[0]) in range(224,240):
            print("multicast")
        else:
            print("unused")
    else:
        print("Неправильный IP-адрес")
    ip = input("Input IP-address again: ")
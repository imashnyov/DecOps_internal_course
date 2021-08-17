'''
1. Запросить у пользователя ввод IP-адреса в формате 10.0.1.1
2. Определить тип IP-адреса.
3. В зависимости от типа адреса, вывести на стандартный поток вывода:
    • „unicast“ - если первый байт в диапазоне 1-223
    • „multicast“ - если первый байт в диапазоне 224-239
    • „local broadcast“ - если IP-адрес равен 255.255.255.255
    • „unassigned“ - если IP-адрес равен 0.0.0.0
    • „unused“ - во всех остальных случаях 
'''
ip = input("Input IP-address: ")
split_ip = ip.split('.')
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

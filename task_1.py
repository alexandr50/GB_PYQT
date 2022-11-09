import os
import  subprocess
import platform
import threading
import time
from pprint import pprint
from ipaddress import ip_address

result = {'Доступные узлы': [], 'Недоступные узлы': []}
DNULL = open(os.devnull, 'w')

def check_is_ipaddress(value):
    try:
        ipv4 = ip_address(value)
    except ValueError:
        raise Exception('Неверный ip адресс')
    return ipv4

def ping(ipv4, result, get_list):
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    response = subprocess.Popen(['ping', param, '1', '-c', '1', str(ipv4)],
                                stdout=subprocess.PIPE)

    if response.wait() == 0:
        result['Доступные узлы'].append(str(ipv4))

        res = f'{ipv4} - Узел доступен'
        if not get_list:
            print(res)
        return res
    else:
        result['Недоступные узлы'].append(str(ipv4))

        res = f'{ipv4} - Узел доступен'
        if not get_list:
            print(res)
        return res


def host_ping(hosts_list, get_list=False):
    print('Начало проверки')
    threads = []
    for host in hosts_list:
        try:
            ipv4 = check_is_ipaddress(host)
        except Exception as e:
            print(f'{host} - {e}, воспринимаю как доменное имя')
            ipv4 = host
        thread = threading.Thread(target=ping, args=(ipv4, result, get_list), daemon=True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if get_list:
        return result

if __name__ == '__main__':
    hosts_list = ['1.1.1.255', '192.168.0.1', '1.1.1.1', 'yandex.ru', 'google.com', 'fuz']

    start = time.time()
    result = host_ping(hosts_list, True)
    end = time.time()
    print(f'total time: {int(end - start)}')
    pprint(result)

































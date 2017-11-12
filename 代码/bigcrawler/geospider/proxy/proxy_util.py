# -*- encoding: utf-8 -*-
import logging

from entities import Proxy
def loadIp():
    ips = []
    lines = []
    with open('../../datafile/ip.txt', 'r') as fr:
        lines = fr.readlines()
        fr.close()

    for line in lines:
        content = line.strip().split('\t')
        item = Proxy(content[0], content[1], content[2])
        # item.display()
        ips.append(item)
    return ips

def get_ips():
    ips = loadIp()
    http = []
    https = []
    for p in ips:
        if p.type == "HTTP":
            http.append(p)
        else:
            https.append(p)
    return http, https

http, https = get_ips()

for p in https:
    logging.log(logging.WARNING, p.display())
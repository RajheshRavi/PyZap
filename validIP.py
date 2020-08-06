def verifyIP(ip):             # For IPv4
    ip = ip.split('.')
    if len(ip) != 4:
        return False
    else:
        for i in ip:
            if int(i) > 255 or int(i) < 0:
                return False
        return True

def VerifyPort(port):
    port = int(port)
    if port < 0 or port > 65535:
        return False
    return True
#print(verify('172.0.0.256'))

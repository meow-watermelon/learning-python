#!/usr/bin/env python3

import socket
import ssl
import sys

def get_tls_cert_exp_date(host, port):
    tls_cert_exp_date = None

    context = ssl.SSLContext()
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('/etc/ssl/certs/ca-bundle.crt')
    context.check_hostname = False

    try:
        req = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    except:
        print('SOCKET ERROR: Failed to wrap socket.')
        tls_cert_exp_date = None
   
    req.settimeout(5)  

    try:
        req.connect((host, port))
    except socket.gaierror:
        print('SOCKET ERROR: [%s] is not resolvable.' %(host))
        tls_cert_exp_date = None
    except socket.timeout:
        print('SOCKET ERROR: Timeout triggered.')
        tls_cert_exp_date = None
    except ConnectionRefusedError:
        print('SOCKET ERROR: Connection refused on [%s]:[%d].' %(host, port))
        tls_cert_exp_date = None
    except ssl.SSLError as e:
        error = e.reason
        print('SSL ERROR: TLS layer error: [%s].' %(error))
        tls_cert_exp_date = None
    except:
        print('SOCKET / SSL ERROR: Unexpected error.')
        tls_cert_exp_date = None

    if tls_cert_exp_date != None:
        tls_cert = req.getpeercert()
        if len(tls_cert) == 0:
            tls_cert_exp_date = 0
        else:
            tls_cert_exp_date = tls_cert['notAfter']

    try:
        req.shutdown(socket.SHUT_RDWR)
    except:
        pass

    req.close()

    return tls_cert_exp_date

print(get_tls_cert_exp_date('www.google.com', 444))

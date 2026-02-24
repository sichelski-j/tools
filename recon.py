import socket
import sys
import datetime
import requests

target = sys.argv[1]
target_url = sys.argv[2]
web_server_found = False
files = ["admin", "login", "test.php", "info.php", "cmd.php"]

try:
    start_t=datetime.datetime.now()
    print(f"Scanning started at: {start_t}")
    for port in range (1,4001):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        x=s.connect_ex((target,port))
        if x==0:
            print(f"Port {port} is open!")
            if port == 80 or port == 443:
                web_server_found = True
        s.close()
    end_t=datetime.datetime.now()
    print(f"Scanning ended at: {end_t}")
    scan_t=end_t-start_t
    print (f"Scanning time: {scan_t}")

    if web_server_found==True:
        for file in files:
            url = target_url + file
            r=requests.get(url, allow_redirects=False)
            if r.status_code==200:
                print(f"[+] URL found: {url}")
            elif r.status_code==301 or r.status_code==302:
                new_location=r.headers.get('Location')
                print(f"[~] Redirection found: {url} -> moves to {new_location}")
            elif r.status_code==403:
                print(f"URL found: {url}, denied access (403)")
    else:
        print("\nNo web server found on port 80 or 443. Skipping dirbuster.")
except KeyboardInterrupt:
    print ("\nExiting program.")
    sys.exit()
import socket
import sys
import datetime
import requests
import argparse

parser = argparse.ArgumentParser(description="My Custom Recon Tool")
parser.add_argument("-t", "--target", help="The target IP address", required=True)
parser.add_argument("-u", "--url", help="The target URL for dirbuster", required=True)

args = parser.parse_args()
target = args.target
target_url = args.url
web_server_found = False
files = ["admin", "login", "test.php", "info.php", "cmd.php"]
filename = f"recon_{target}.txt"

f = open(filename, "w")

try:
    start_t=datetime.datetime.now()
    print(f"Starting scan on {target}, please wait.")
    print(f"Scanning started at: {start_t}", file=f)
    for port in range (1,1001):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        x=s.connect_ex((target,port))
        if x==0:
            print(f"Port {port} is open!", file=f)
            if port == 80 or port == 443:
                web_server_found = True
        s.close()
    end_t=datetime.datetime.now()
    print(f"Scanning ended at: {end_t}", file=f)
    scan_t=end_t-start_t
    print (f"Scanning time: {scan_t}", file=f)

    if web_server_found==True:
        print(f"Starting dirbuster on {target_url}, please wait.")
        for file in files:
            url = target_url + file
            r=requests.get(url, allow_redirects=False)
            if r.status_code==200:
                print(f"[+] URL found: {url}", file=f)
            elif r.status_code==301 or r.status_code==302:
                new_location=r.headers.get('Location')
                print(f"[~] Redirection found: {url} -> moves to {new_location}", file=f)
            elif r.status_code==403:
                print(f"URL found: {url}, denied access (403)", file=f)
    else:
        print("\nNo web server found on port 80 or 443. Skipping dirbuster.", file=f)
    f.close()
    print(f"Scan saved to the file named recon_{target}.txt")
except KeyboardInterrupt:
    print ("\nExiting program.")
    sys.exit()
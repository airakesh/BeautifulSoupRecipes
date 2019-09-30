''' Get Geolocation(Country) and hostname by passing a file having bunch of IPs as the argument form commandline. Example- python GeoIP.py path-to-file-containing-ips/ips_list.txt'''                                                                                                                                                                     import re

import os
import sys
import subprocess
import socket

ips_file = sys.argv[1]

#  The regular expression for validating an IP-address                                                                                                                                                              
pattern = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''

def getGeoHost():
    fp = open(ips_file, 'rb')
    for line in fp:
        line = line.strip()
        addr = line.decode('utf-8')
        regex = re.compile(pattern)
        match = regex.match(addr)
        ## Get hostname by IP address                                                                                                                                                                               
        try:
            host = socket.gethostbyaddr(addr)
            hostname = host[0]
        # Print Unknown no hostname is available                                                                                                                                                                    
        except:
            hostname = 'Unknown'

        # Get geolocation by IP address                                                                                                                                                                             
        get_geo_cmd = 'geoiplookup ' + addr
        geo_str = subprocess.check_output(get_geo_cmd, shell=True)
        geo = geo_str.decode('utf-8')

        # Match country name pattern                                                                                                                                                                                
        geo_pattern = '''^(GeoIP Country Edition: ([A-Z]{2})\, (.*))'''
        geo_regex = re.compile(geo_pattern)
        country_match = re.match(geo_pattern, geo)
        # Check country name is available and if not, print 'Unknown'                                                                                                                                               
        if country_match != '' and geo_pattern:
            try:
                country = country_match.group(3)
            except:
                country = 'Unknown'
        # Clubbing together in format 'IP|Country|Hostname' data                                                                                                                                                    
        geo_hostname = addr + ' | ' + country + ' | ' + hostname
        print geo_hostname

# Driver code                                                                                                                                                                                                       
if __name__ == "__main__":
    ips_detail_list = getGeoHost()

'''
Python program scrapes data from website as a source and changes identity (IP address) - using proxies that rotate an IP and fake User Agents using Python 3.7
'''
from urllib.request import Request, urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random

# Generate a random user agent
ua = UserAgent()
# Declaring proxies list to store data [ip, port]
proxies = []
# Declaring the lists to store data of IPs
ips = []

# Funciton to retrieve a random index proxy and delete it if not working
def random_proxy():
    return random.randint(0, len(proxies) - 1)

# scrape proxies
def proxy():
    # Retrieve latest 100 proxies ips
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    # Store proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
            'ip': row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
        })
    # Choose a random proxy
    proxy_index = random_proxy()
    proxy = proxies[proxy_index]

    # Read ips list from the file: ~/sample_ips.txt
    for n in range(1, 100):
        with open('sample_ips.txt', 'r') as fp:
            for ip in fp:
                # request to scraping site
                ips_req = Request('https://whatismyipaddress.com/ip/' + ip)

                # set to rotate fake user-agents in the header
                ips_req.add_header('User-Agent', ua.random)

                # set proxy [ip:port]
                ips_req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')

                # Every 10 requests, generate a new proxy
                if n % 10 == 0:
                    proxy_index = random_proxy()
                    proxy = proxies[proxy_index]

                # Make the call
                try:
                    my_ip = urlopen(ips_req).read().decode('utf8')
                    print('#' + str(n) + ': ' + my_ip)
                except:  # If error, delete this proxy and find another one
                    del proxies[proxy_index]
                    print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')

                    proxy_index = random_proxy()
                    proxy = proxies[proxy_index]

                    # Check response code and exit if throws an error
                    try:
                        html_doc = urlopen(ips_req).read().decode('utf8')
                    except URLError as e:
                        if hasattr(e, 'reason'):
                            print('We failed to reach a server.')
                            print('Reason: ', e.reason)
                        elif hasattr(e, 'code'):
                            print('The server couldn\'t fulfill the request.')
                            print('Error code: ', e.code)
                    else:
                        # Parse the content of the request with BeautifulSoup if request is successful
                        soup = BeautifulSoup(html_doc, 'html5lib')

                        table_doc = soup.find(id="section_left_3rd")

                        # save ips detail in the dict(array)
                        for td in table_doc.table.find_all('tbody'):
                            ips.append({
                                'ip': td.find_all('td')[0].string,
                                'hostname': td.find_all('td')[2].string,
                                'isp': td.find_all('td')[4].string,
                                'organizatoin': td.find_all('td')[5].string,
                                'assignment': td.find_all('td')[8].string,
                            })

# Driver code
if __name__ == '__main__':
    proxy()
    print(proxy)

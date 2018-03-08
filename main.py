from time import sleep
from bs4 import BeautifulSoup
import ssl
import urllib2
import mechanize
import re
import networkx as nx
import matplotlib.pyplot as plt

pat = re.compile('^(http(.)?://)([^/])*?([^.])*?(.htm(l)?|/)?$')  # DNT!!!
seed = unicode('http://info.cern.ch/')  # The home of the first page on the web.
queue = [seed]
links = {seed}
G = nx.MultiGraph()
plt.ion()
while len(queue) > 0:
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.set_handle_refresh(False)
    browser.addheaders = [('User-agent', "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36")]  # DNT!!!
    print "next: " + queue[0]
    try:
        browser.open(queue[0], timeout=1200)
        soup = BeautifulSoup(browser.response().read(), "html5lib")
        # soup.prettify()
        for k in soup.find_all('a'):
            lnk = unicode(k.get('href'))
            if pat.match(lnk):
                # print k.get('href')
                G.add_edge(queue[0], lnk)
                if lnk not in links:
                    queue.append(lnk)
                    links.add(lnk)
            plt.pause(0.01)
    except (mechanize.HTTPError, mechanize.URLError, ssl.CertificateError, ssl.SSLError, urllib2.URLError) as error:
        print "\t" + str(error)
        # pass
    finally:
        nx.draw_networkx(G,
                         pos=nx.spring_layout(G),
                         with_labels=False,
                         font_weight='bold',
                         node_size=2,
                         linewidths=None,
                         width=0.2,
                         style='dotted')
        plt.pause(0.5)
        browser.close()
    del queue[0]
    sleep(0.001)
while True:
    plt.pause(0.05)

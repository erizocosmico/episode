#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""episode

Usage:
  episode <show_url> [-c <content_in_name>] [-m]
  episode <show_url> (-s|-o) <season> [-c <content_in_name>] [-m]
  episode <show_url> -s <season> (-e|-f) <episode> [-c <content_in_name>] [-m]
  episode (-h | --help)

Options:
  -h --help     Show this screen.
  -s            Download from the specified season.
  -o            Download from the Xth season on.
  -e            Just the selected episode.
  -f            From the selected episode on.
  -c            Search content in episode name (e.g: 720p)
  -m            Magnet link preferred.

"""

from __future__ import print_function, with_statement
from pyquery import PyQuery as pq
from docopt import docopt
import requests
import sys
import os
import re
__version__ = '1.0.2'

args = docopt(__doc__, version=__version__)
downloaded = []

def parse_episode_name(text):
    x_notation = re.compile('\d{1,2}x\d{2}')
    s_e_notation = re.compile('S\d{2}E\d{2}')
    name_x = x_notation.findall(text)
    name_s_e = s_e_notation.findall(text)
    
    if name_x:
        return name_x[0]
    
    if name_s_e:
        nums = re.compile('\d+').findall(name_s_e[0])
        return "%dx%s" % (int(nums[0]), nums[1])
        
    return None
    
def build_episode_name(season, episode):
    return "%dx%s%d" % (season, '' if episode >= 10 else '0', episode)
    
def get_show_url(name):
    try:
        r = requests.get('http://eztv.it/showlist/')
        if r.status_code != 200:
            raise Exception
        html = pq(r.text)
        table = html('table').eq(1)
        for tr in table('tr'):
            row = table(tr)
            col = row('td').eq(0)
            a = col('a').eq(0)
            if not a:
                continue
            if a.text().lower() == name.lower():
                return 'http://eztv.it' + a.attr('href')
    except:
        print('Error retrieving eztv url for given show.')
        sys.exit(2)
        
    return None

if __name__ == '__main__':
    try:
        url = args['<show_url>']
        content_in_name = args['<content_in_name>']
        magnet_preferred = args['-m']
        download_season = args['-s']
        download_episode = args['-e']
        download_from = args['-f']
        download_season_from = args['-o']
        if download_season:
            try:
                season = int(args['<season>'])
            except:
                season = None
            if download_episode or download_from:
                try:
                    episode = int(args['<episode>'])
                except:
                    episode = None
        search_content = args['-c']

        if not 'http' in url or not 'eztv.it/shows/' in url:
            url = get_show_url(url)
        else:
            try:
                req = requests.get(url)
                if not 'bitcoin:1EZTVaGQ6UsjYJ9fwqGnd45oZ6HGT7WKZd' in req.text:
                    raise Exception
            except:
                url = get_show_url(url)
        if not url:
            print('Unable to find episodes for the specified show.')
            sys.exit(2)
        
        try:
            req = req
        except NameError:
            req = requests.get(url)

        show_name = filter(None, url.split('/'))[-1]

        content = pq(req.text)
        torrents_table = pq(content('table').eq(6))
        for tr in torrents_table('tr')[::-1]:
            table_row = torrents_table(tr)
            _episode = table_row('td').eq(1).text()
            if search_content:
                if not content_in_name in _episode:
                    continue
            if not _episode or _episode == 'Episode Name':
                continue
            name = parse_episode_name(_episode)
            if not name or name in downloaded:
                continue
          
            if download_season or download_season_from:
                if download_episode:
                    if name != build_episode_name(season, episode):
                        continue
                elif download_from:
                    s, ep = name.split('x')
                    if not (int(s) == season and int(ep) >= episode):
                        continue
                else:
                    s, ep = name.split('x')
                    if download_season_from and int(s) < season:
                        continue
                    elif int(s) != season:
                        continue
    
            torrents_column = table_row('td').eq(2)

            if magnet_preferred:
                magnet = torrents_column('a').eq(0).attr('href')
                os.system("open '%s' > /dev/null" % magnet)
                print(' * Downloading episode magnet: %s' % name)
    
            first = True
            for a in torrents_column('a'):
                if first:
                    first = False
                    continue
        
                if name in downloaded:
                    break
                torrent_url = torrents_column(a).attr('href')
                r = requests.get(torrent_url)
                if r.status_code == 200:
                    with open('%s-%s.torrent' % (show_name, name), 'w') as f:
                        f.write(r.content)
                    print(' * Downloading episode: %s' % name)
                    downloaded.append(name)
                    break
        
            if not name in downloaded and not magnet_preferred:
                magnet = torrents_column('a').eq(0).attr('href')
                os.system("open '%s' > /dev/null" % magnet)
                print(' * Downloading episode magnet: %s' % name)
    except:
        print("Unknown error occurred.")
        sys.exit(2)

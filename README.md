episode
=======

Downloading torrent files from EZTV shows made easy.

Usage
-----
```bash
episode

Usage:
  episode <eztv_show_url> [-c <content_in_name>] [-m]
  episode <eztv_show_url> -s <season> [-c <content_in_name>] [-m]
  episode <eztv_show_url> -s <season> (-e|-f) <episode> [-c <content_in_name>] [-m]
  episode (-h | --help)

Options:
  -h --help     Show this screen.
  -s            Download from the specified season.
  -e            Just the selected episode.
  -f            From the selected episode on.
  -c            Search content in episode name (e.g: 720p)
  -m            Magnet link preferred.
```

Examples
------
```bash
episode http://eztv.it/shows/78/dexter/
episode http://eztv.it/shows/78/dexter/ -s 2 -f 6
episode http://eztv.it/shows/78/dexter/ -s 5
episode http://eztv.it/shows/78/dexter/ -m
episode http://eztv.it/shows/78/dexter/ -c '720p'
```

Install
------
```bash
sudo curl https://raw.github.com/mvader/episode/master/episode.py -o /usr/local/bin/episode;
sudo chmod +x /usr/local/bin/episode
```


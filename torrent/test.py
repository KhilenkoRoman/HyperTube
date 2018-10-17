import libtorrent as lt
import time
import sys

link = "magnet:?xt=urn:btih:5097C680F4F429FF795C9EEC4EA8B30456211618&amp;dn=Skyscraper+%282018%29+%5B720p%5D+%5BYTS.AG%5D&amp;tr=udp%3A%2F%2Fglotorrents.pw%3A6969%2Fannounce&amp;tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&amp;tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&amp;tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&amp;tr=udp%3A%2F%2Fp4p.arenabg.ch%3A1337&amp;tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337"


ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})

info = lt.torrent_info('../media/torrent_files/3175.torrent')
h = ses.add_torrent({'ti': info, 'save_path': '.'})
print('starting', h.name())

while not h.is_seed():
    s = h.status()

    print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % \
          (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
           s.num_peers, s.state), end=' ')

    alerts = ses.pop_alerts()
    for a in alerts:
        if a.category() & lt.alert.category_t.error_notification:
            print(a)

    sys.stdout.flush()

    time.sleep(1)

print(h.name(), 'complete')

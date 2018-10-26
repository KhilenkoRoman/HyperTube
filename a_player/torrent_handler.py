import libtorrent as lt
import time
import sys
# from django.conf import settings
from django.conf import settings


# ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})


# info = lt.torrent_info('../media/torrent_files/3175.torrent')
# h = ses.add_torrent({'ti': info, 'save_path': '.'})
# print('starting', h.name())
#
# while not h.is_seed():
#     s = h.status()
#
#     print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % \
#           (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
#            s.num_peers, s.state), end=' ')
#
#     alerts = ses.pop_alerts()
#     for a in alerts:
#         if a.category() & lt.alert.category_t.error_notification:
#             print(a)
#
#     sys.stdout.flush()
#
#     time.sleep(1)
#
# print(h.name(), 'complete')

# def add_torrent(ses, filename, options):

def add_torrent(torrent_model):
    print(settings.TORRENT_SESION)
    if not settings.TORRENT_SESION:
        settings.TORRENT_SESION = lt.session({'listen_interfaces': '0.0.0.0:6881'})
    print(settings.TORRENT_SESION)

    path = settings.MEDIA_ROOT + '/' + str(torrent_model.torrent_file)
    info = lt.torrent_info(path)
    print(path)

    if torrent_model.quality == 0:
        info.files().set_name(torrent_model.film.name + "_720p")
    else:
        info.files().set_name(torrent_model.film.name + "_1080p")

    thd = settings.TORRENT_SESION.add_torrent({'ti': info, 'save_path': settings.MEDIA_ROOT + '/video'})
    settings.TORRENTS.append(thd)


def torrent_info():
    print(settings.TORRENT_SESION)
    print(settings.TORRENTS)

    h = settings.TORRENTS[0]

    while not h.is_seed():
        s = h.status()

        print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % \
              (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state), end=' ')

        alerts = settings.TORRENT_SESION.pop_alerts()
        for a in alerts:
            if a.category() & lt.alert.category_t.error_notification:
                print(a)

        sys.stdout.flush()

        time.sleep(1)

    print(h.name(), 'complete')

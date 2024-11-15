from time import sleep
import libtorrent as lt
import tempfile
import os.path as path
import shutil


def magnet2torrent(magnet, output_name):
    tempdir = tempfile.mkdtemp()
    ses = lt.session()
    params = {
        'save_path': tempdir,
        'storage_mode': lt.storage_mode_t(2)
        #'paused': False,
        #'auto_managed': True,
        #'duplicate_is_error': True
    }
    
    handle = lt.add_magnet_uri(ses, magnet, params)

    print("Downloading Metadata (this may take a while)")
    counter = 0
    while (not handle.has_metadata()):
        if counter > 60:
            ses.pause()
            return False
        sleep(1)
        counter += 1
    ses.pause()
    print("Done")

    torinfo = handle.get_torrent_info()
    torfile = lt.create_torrent(torinfo)

    output = path.abspath(torinfo.name() + ".torrent")

    if output_name:
        if path.isdir(output_name):
            output = path.abspath(path.join(
                output_name, torinfo.name() + ".torrent"))
        elif path.isdir(path.dirname(path.abspath(output_name))):
            output = path.abspath(output_name)

    print("Saving torrent file here : " + output + " ...")
    torcontent = lt.bencode(torfile.generate())
    f = open(output, "wb")
    f.write(lt.bencode(torfile.generate()))
    f.close()
    print("Saved! Cleaning up dir: " + tempdir)
    ses.remove_torrent(handle)
    shutil.rmtree(tempdir)
    return True



if __name__ == "__main__":
    magnet2torrent("magnet:?xt=urn:btih:86459097095BE9314C16FE60694212842805BA56&dn=Spider-Man%3A+Across+the+Spider-Verse&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2710%2Fannounce&tr=udp%3A%2F%2Fp4p.arenabg.ch%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.cyberia.is%3A6969%2Fannounce&tr=http%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce", "./tt9362722.torrent")
from upload.models import File, make_dir
from upload.forms import save_sizes
import urllib.request
import urllib.error
import urllib.parse
import time
import os
import os.path


def download(url, file):
    """Handle downloading of files from any URL, delete file recerds when 404.
    """
    try:
        print(url)
        return urllib.request.urlopen(url, timeout=15).read()
    except urllib.error.HTTPError as e:
        print(e.code, url)
        file.delete()
        time.sleep(.5)
    except urllib.error.URLError as e:
        print(e.args, url)
    return ''


def get_missing_file(file, url):
    """Check file exists, download if not.
    """
    path = file.path()
    if file.col_id and not os.path.exists(path):
        make_dir(path)
        data = download(url, file)
        if data:
            f = open(path, 'wb')
            f.write(data)
            f.close()


def add_files(obj, urls_alts):
    """Add files to object from a list of URLs
    urls_alts = ((url, alt), (url2, alt2))

    Iterates over the datastructure, creates file objects,
    downloads missing files.
    """
    for url, alt in urls_alts:
        fn = url.split('/')[-1]
        file = File(alt=alt, col=obj, fn=fn)
        file.save()
        get_missing_file(file, url)
        try:
            save_sizes(file)
        except IOError:
            os.remove(file.path())
            file.delete()

# encoding: utf-8
import os
import urllib2
import csv
import hashlib

from nose.tools import eq_

PYPI_MD5_URL = 'http://pypi.python.org/pypi?:action=show_md5&digest='

PYPI_DOWNLOADS = {
    # filename: md5sum
    'distribute-0.6.49.tar.gz': '89e68df89faf1966bcbd99a0033fbf8e',
    'virtualenv-1.10.1.tar.gz': '3a04aa2b32c76c83725ed4d9918e362e',
    'virtualenvwrapper-4.0.tar.gz': '78df3b40735e959479d9de34e4b8ba15',
}


def test_tarball_names():
    tarballs = set()
    with open('versions.csv', 'r') as fo:
        reader = csv.reader(fo)
        for name, version, url, digest in reader:
            if name.startswith('_'):
                continue
            tarballs.add(os.path.basename(url))

    eq_(tarballs, set(PYPI_DOWNLOADS.keys()))


def test_shasum():
    with open('versions.csv', 'r') as fo:
        reader = csv.reader(fo)
        for name, version, url, digest in reader:
            if name.startswith('_'):
                continue
            sha1 = hashlib.sha1()
            sha1.update(urllib2.urlopen(url).read())
            eq_(digest, sha1.hexdigest())


def test_md5_url_exists():
    for ball, md5sum in PYPI_DOWNLOADS.iteritems():
        url = PYPI_MD5_URL + md5sum
        try:
            urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            assert False, "Failed to open %s: %s %s" % (url, type(e), e)

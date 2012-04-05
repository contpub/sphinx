# -*- coding: utf-8 -*-
"""
    sphinx.builders.mobi
    ~~~~~~~~~~~~~~~~~~~~

    Build epub files.
    Originally derived from epub.py.

    :copyright: Copyright 2007-2011 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import os

from sphinx.builders.epub import EpubBuilder

_content_template = u'''\
<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0"
      unique-identifier="%(uid)s">
  <metadata xmlns:opf="http://www.idpf.org/2007/opf"
        xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:language>%(lang)s</dc:language>
    <dc:title>%(title)s</dc:title>
    <dc:creator opf:role="aut">%(author)s</dc:creator>
    <dc:publisher>%(publisher)s</dc:publisher>
    <dc:rights>%(copyright)s</dc:rights>
    <dc:identifier id="%(uid)s" opf:scheme="%(scheme)s">%(id)s</dc:identifier>
    <dc:date>%(date)s</dc:date>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml" />
%(files)s
  </manifest>
  <spine toc="ncx">
%(spine)s
  </spine>
  <guide>
    <reference type="toc" title="Table of Contents" href="contents.html" />
    <reference type="text" title="Overview" href="index.html" />
  </guide>
</package>
'''

_mimetype_template = 'application/x-mobipocket-ebook'

class MobiBuilder(EpubBuilder):
    """
    Builder that outputs mobi files.

    It creates the metainfo files container.opf, toc.ncx, mimetype, and
    META-INF/container.xml.  Afterwards, the kindlegen utility is used
    to generate the mobi file.
    """
    name = 'mobi'

    def init(self):
        EpubBuilder.init(self)

    # Finish by building the mobi file
    def handle_finish(self):
        """Create the metainfo files and finally the mobi."""
        EpubBuilder.handle_finish(self)
        _epub_file = os.path.join(self.outdir,
            self.config.epub_basename + '.epub')
        os.system("kindlegen -c1 -rebuild -verbose %s" % _epub_file)

    def get_theme_config(self):
        return self.config.mobi_theme, {}

    def build_content(self, outdir, outname):
        """Write the metainfo file content.opf It contains bibliographic data,
        a file list, the spine (the reading order) and the guide (first page
        and html version of the toc).
        """

        EpubBuilder.build_content(self, outdir, outname,
            content_template=_content_template)

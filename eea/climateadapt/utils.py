""" Generic utilities
"""

import logging

from DateTime import DateTime

# import time


logger = logging.getLogger('eea.climateadapt')


def _unixtime(d):
    """ Converts a datetime to unixtime
    """

    if isinstance(d, DateTime):
        d = d.utcdatetime()

    if d:
        return d.isoformat()

    return

    # try:
    #     return int(time.mktime(d.utctimetuple()))
    # except AttributeError:
    #     logger.exception('Error converting to unix datetime %r', d)
    #
    #     return ""


def shorten(t, to=254):
    """ Shortens text and adds elipsis
    """

    if isinstance(t, unicode):
        el = u'...'
    else:
        el = '...'

    if len(t) > to - 3:
        t = t[:to - 3] + el

    return t

# -*- coding: utf-8 -*-

import re


class NikeNewSneaker(object):

    def __init__(self, _id):
        self._id = _id
        self.img = None
        self.href = None
        self.release_date = None
        self._release_time = None

    @property
    def release_time(self):
        return self._release_time

    @release_time.setter
    def release_time(self, raw_text):
        """ Parse the text from website and convert it to datetime objects """
        # TODO convert to Datetime objects
        if not raw_text:
            return
        regex_pattern = re.compile('预计(\S*)\s*开始发售')
        match = regex_pattern.match(raw_text)
        if match:
            self._release_time = match.group(1)
        else:
            self._release_time = raw_text

    def __str__(self):
        message = "{}\n{}\n{} - {}".format(self._id, self.href, self.release_date, self._release_time)
        return message

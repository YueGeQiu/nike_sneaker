# -*- coding: utf-8 -*-


class NikeNewSneaker(object):

    def __init__(self, _id):
        self._id = _id
        self.img = None
        self.href = None
        self.release_date = None
        self.release_time = None

    def __str__(self):
        message = "{}\n{}\n{} - {}".format(self._id, self.href, self.release_date, self.release_time)
        return message

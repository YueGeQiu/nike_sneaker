# -*- coding: utf-8 -*-

from nike_sneaker.sneaker import NikeNewSneaker


def test_release_date():
    sneaker = NikeNewSneaker('unit-test')
    assert sneaker._id == 'unit-test'
    raw_string = '预计下午15:00 开始发售'
    sneaker.release_time = raw_string
    assert sneaker.release_time == '下午15:00'

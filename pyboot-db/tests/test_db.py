from pyboot.db.app import Initializer


def test_initializer():
    Initializer()


def test_failed():
    assert False, "This test is designed to fail"

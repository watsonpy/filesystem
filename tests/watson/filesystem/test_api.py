# -*- coding: utf-8 -*-
from pytest import raises
from watson.filesystem import Filesystem
from tests.watson.filesystem.support import MockBackend


class TestApi(object):

    def test_no_backend(self):
        with raises(TypeError):
            Filesystem()

    def test_with_backend(self):
        assert Filesystem(MockBackend())

    def test_read(self):
        fs = Filesystem(MockBackend())
        assert fs.read(None)
        assert fs[None]

    def test_exists(self):
        fs = Filesystem(MockBackend())
        assert fs.exists(None)
        assert None in fs

    def test_write(self):
        fs = Filesystem(MockBackend())
        assert fs.write(None, None)
        fs['test'] = 'test'

    def test_append(self):
        fs = Filesystem(MockBackend())
        assert fs.append(None, None)

    def test_delete(self):
        fs = Filesystem(MockBackend())
        assert fs.delete(None)

    def test_move(self):
        fs = Filesystem(MockBackend())
        assert fs.move(None, None)

    def test_copy(self):
        fs = Filesystem(MockBackend())
        assert fs.copy(None, None)

    def test_create(self):
        fs = Filesystem(MockBackend())
        assert fs.create(None)
        assert fs.create(None, is_dir=True)


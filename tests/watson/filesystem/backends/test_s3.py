# -*- coding: utf-8 -*-
import os
import pytest
from pytest import raises
from watson.filesystem import Filesystem, backends, exceptions


@pytest.mark.skipif(
    not os.environ.get('AWS_ACCESS_KEY_ID'), reason='No AWS credentials')
class TestS3(object):

    def setup(self):
        self.fs = Filesystem(backends.S3(
            aws_access_key=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            bucket='watson-filesystem'),
        )

    def test_write(self):
        self.fs.write('test.txt', 'this is a test')
        assert self.fs.exists('test.txt')

    def test_read(self):
        self.fs.write('test.txt', 'test')
        content = self.fs.read('test.txt')
        assert content == b'test'

    def test_read_not_found(self):
        with raises(exceptions.NotFoundError):
            self.fs.read('not-found')

    def test_append(self):
        self.fs.write('test.txt', 'testing')
        assert self.fs.read('test.txt')
        self.fs.append('test.txt', b' with new test copy')
        assert self.fs.read('test.txt') == b'testing with new test copy'

    def test_create_delete(self):
        self.fs.create('blah.txt')
        assert self.fs.exists('blah.txt')
        self.fs.delete('blah.txt')
        assert not self.fs.exists('blah.txt')
        self.fs.create('directory', is_dir=True)
        assert self.fs.exists('directory/')
        self.fs.delete('directory/')
        assert not self.fs.exists('directory/')

    def test_delete_recursive(self):
        self.fs.create('subdirectory/file.txt')
        assert self.fs.exists('subdirectory/file.txt')
        self.fs.delete('subdirectory/file.txt')
        assert not self.fs.exists('subdirectory/file.txt')

    def test_move(self):
        self.fs.create('to_move.txt')
        self.fs.move('to_move.txt', 'moved.txt')
        assert not self.fs.exists('to_move.txt')
        assert self.fs.exists('moved.txt')
        self.fs.delete('moved.txt')

    def test_copy(self):
        self.fs.create('copy.txt')
        self.fs.copy('copy.txt', 'copied.txt')
        assert self.fs.exists('copy.txt')
        assert self.fs.exists('copied.txt')
        self.fs.delete('copy.txt')
        self.fs.delete('copied.txt')

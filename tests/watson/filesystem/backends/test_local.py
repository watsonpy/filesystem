# -*- coding: utf-8 -*-
import os
from pytest import raises
from watson.filesystem import Filesystem, backends


class TestLocal(object):

    def setup(self):
        self.fs = Filesystem(backends.Local())
        self.output_path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(__file__)))), '_output')

    def file(self, path):
        return os.path.join(self.output_path, path)

    def test_factory(self):
        fs = backends.Local.factory()
        assert isinstance(fs, Filesystem)
        assert isinstance(fs.backend, backends.Local)

    def test_read(self):
        assert self.fs.read(__file__).startswith('# -*- coding:')

    def test_read_not_found(self):
        with raises(FileNotFoundError):
            self.fs.read('../support.py')

    def test_exists(self):
        assert self.fs.exists(__file__)
        assert not self.fs.exists('../support.py')
        assert __file__ in self.fs

    def test_write(self):
        path = self.file('test')
        self.fs.write(path, 'test')
        assert self.fs.exists(path)
        assert self.fs.read(path) == 'test'
        non_existent_path = self.file('testing/test')
        self.fs.write(non_existent_path, 'test')
        assert self.fs.exists(non_existent_path)
        self.fs.delete(non_existent_path)

    def test_append(self):
        path = self.file('test')
        self.fs.append(path, 'test')
        assert self.fs.read(path) == 'testtest'

    def test_create_delete(self):
        path = self.file('test-delete')
        self.fs.delete(path)
        assert not self.fs.exists(path)
        self.fs.create(path)
        assert self.fs.exists(path)
        self.fs.delete(path)
        assert not self.fs.exists(path)
        path = self.file('test-delete-folder')
        self.fs.create(path, is_dir=True)
        self.fs.delete(path)

    def test_delete_recursive(self):
        path = self.file('testing/sub/folder')
        self.fs.create(path, is_dir=True)
        assert self.fs.exists(path)
        self.fs.delete(self.file('testing'))
        assert not self.fs.exists(path)

    def test_move(self):
        path = self.file('testing')
        new_path = self.file('testing_new')
        self.fs.create(path)
        self.fs.move(path, new_path)
        assert not self.fs.exists(path)
        assert self.fs.exists(new_path)
        self.fs.delete(new_path)

    def test_copy(self):
        path = self.file('testing')
        new_path = self.file('testing_new')
        self.fs.create(path)
        self.fs.copy(path, new_path)
        assert self.fs.exists(path)
        assert self.fs.exists(new_path)
        self.fs.delete(path)
        self.fs.delete(new_path)
        dir_path = self.file('testing/sub/directory')
        new_dir_path = self.file('testing2')
        self.fs.create(dir_path, is_dir=True)
        self.fs.copy(dir_path, new_dir_path)
        assert self.fs.exists(new_dir_path)
        self.fs.delete(dir_path)
        self.fs.delete(new_dir_path)

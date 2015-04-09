# -*- coding: utf-8 -*-
from watson.filesystem.backends import abc


class MockBackend(abc.Backend):

    def read(self, file, options=None):
        return True

    def exists(self, path):
        return True

    def write(self, file, content, options=None):
        return True

    def append(self, file, content, options=None):
        return True

    def delete(self, file):
        return True

    def move(self, path, new_path):
        return True

    def copy(self, path, new_path):
        return True

    def create(self, path, is_dir=False):
        return True

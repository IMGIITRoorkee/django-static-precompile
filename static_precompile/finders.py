import os
import subprocess

import settings

from django.contrib.staticfiles.finders import BaseFinder
from django.core.files.storage import FileSystemStorage
from django.conf import settings as django_settings
from django.utils._os import safe_join

class HandlebarsFinder(BaseFinder):
  def __init__(self):
    self.root = safe_join(settings.CACHE_ROOT, 'HANDLEBARS_CACHE/')
    self.storage = FileSystemStorage(location=self.root)
    self.storage.prefix = ''
    self.file_name = 'templates.js'

  def find(self, path, all=False):
    if path.endswith(self.file_name):
      dir_path = path[:-len(self.file_name)]
      dir_path_splits = dir_path.split('/')
      if len(dir_path_splits)>=1 and dir_path_splits[0] == 'handlebars':
        dir_path_splits = dir_path_splits[1:]
      app = '_'.join(filter(lambda x:x, dir_path_splits))
      if app:
        namespace = 'Handlebars.' + app + '_templates'
      else:
        namespace = 'Handlebars.templates'
      cache_path = safe_join(self.root, dir_path)
      template_path = safe_join(cache_path, self.file_name)
      for STATIC_PATH in django_settings.STATICFILES_DIRS:
        source_path = safe_join(STATIC_PATH, dir_path)
        if os.path.exists(source_path):
          if not os.path.exists(cache_path):
            os.makedirs(cache_path)
          if not os.path.exists(template_path) or\
              os.path.getmtime(template_path) < os.path.getmtime(source_path):
            command = ['handlebars', '-m', '-e', settings.HANDLEBARS_EXTENSION,
                       '-n', namespace, source_path, '-f', template_path]
            subprocess.call(command)
          return template_path
    return []

  def list(self, ignore_patterns):
    for STATIC_PATH in django_settings.STATICFILES_DIRS:
      for root, dirs, files in os.walk(STATIC_PATH):
        handlebars_files = False
        for f in files:
          if f.endswith('.' + settings.HANDLEBARS_EXTENSION):
            handlebars_files = True
            break
        if handlebars_files:
          path = safe_join(root, self.file_name)
          path = path.split(STATIC_PATH)[1][1:]
          # create cache
          self.find(path)
    for root, dirs, files in os.walk(self.root):
      for f in files:
        if f == self.file_name:
          path = safe_join(root, f)
          path = path.split(self.root)[1][1:]
          yield path, self.storage

class SassFinder(BaseFinder):
  def __init__(self):
    self.root = safe_join(settings.CACHE_ROOT, 'SASS_CACHE/')
    self.storage = FileSystemStorage(location=self.root)
    self.storage.prefix = ''

  def find_imports(self, path, STATIC_PATH, done):
    result = False
    with open(path, 'r') as f:
      for line in f:
        if line.startswith('@import'):
          import_file = eval(line[8:])
          import_path = os.path.join(os.path.dirname(path),import_file)
          import_path = os.path.abspath(import_path)
          rel_path = import_path.split(STATIC_PATH)[1][1:]+'.css'
          if not import_path in done:
            if self.find(rel_path, done=done, check=True) == True:
              result = True
            done.append(import_path)
    return result

  def find(self, path, all=False, done=None, check=False):
    if done is None:
      done = []
    if path.endswith('.css'):
      cache_path = safe_join(self.root, path)
      cache_dir_path = '/'.join(cache_path.split('/')[:-1])
      for STATIC_PATH in django_settings.STATICFILES_DIRS:
        source_path = safe_join(STATIC_PATH, path[:-4]+'.'+
                        settings.SASS_EXTENSION)
        if os.path.exists(source_path):
          if not os.path.exists(cache_dir_path):
            os.makedirs(cache_dir_path)
          if self.find_imports(source_path, STATIC_PATH, done=done) or\
              not os.path.exists(cache_path) or\
              os.path.getmtime(cache_path) < os.path.getmtime(source_path):
              command = ['sass', '-I', STATIC_PATH, '--cache-location',
                  safe_join(settings.CACHE_ROOT,'.sass-cache/')]+\
                  (['--compass'] if settings.USE_COMPASS else [])+\
                  [source_path, cache_path]
              subprocess.call(command)
              if check:
                return True
          return cache_path
    return []

  def list(self, ignore_patterns):
    for STATIC_PATH in django_settings.STATICFILES_DIRS:
      for root, dirs, files in os.walk(STATIC_PATH):
        for f in files:
          if f.endswith('.'+settings.SASS_EXTENSION):
            path = safe_join(root, f)
            path = path.split(STATIC_PATH)[1][1:]
            # create cache
            path = path[:-5]+'.css'
            self.find(path)
    for root, dirs, files in os.walk(self.root):
      for f in files:
        path = safe_join(root, f)
        path = path.split(self.root)[1][1:]
        yield path, self.storage

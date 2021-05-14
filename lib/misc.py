import os, errno
import log

def chop(s, maxlen = 20, suffix = ''):
  if len(s) > maxlen:
    return s[:maxlen-len(suffix)] + suffix
  else:
    return s

def pad_to_length(s, width):
  if width <= len(s):
    return s
  else:
    return s + ' ' * (width - len(s))

def mkdirs(newdir):
  return os.system('mkdir -p "%s"' % newdir) == 0

def rmdirs(dir):
  if not os.path.exists(dir):
    return True

  if not os.path.isdir(dir):
    log.printerr('\'%s\': not a directory' % dir)
    return False

  # First, remove all children of dir
  ls = os.listdir(dir)
  ok = True
  for file in ls:
    full = os.path.join(dir, file)
    if os.path.isdir(full):
      if not rmdirs(full):
        ok = False
    else:
      try:
        os.remove(full)
      except OSError as e:
        log.printerr('could not remove file \'%s\'' % full)
        ok = False

  # Finally, remove the empty dir itself
  if ok:
    try:
      os.rmdir(dir)
    except OSError as e:
      log.printerr('could not remove directory \'%s\'' % dir)
      ok = False
  return ok

def read_file_contents(filename):
  try:
    f = open(filename, 'r')
    return f.read()
  except OSError as e:
    log.printerr('Unable to read file \'%s\'' % filename)
    return None

def write_file_contents(filename, contents):
  try:
    f = open(filename, 'w')
    f.write(contents)
    f.close()
    return True
  except OSError as e:
    log.printerr('Unable to write file \'%s\'' % filename)
    return False

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def cmp(a, b):
  return (a > b) - (a < b)

#
# Python Git library
#
import os

def quote_string(s):
  s = s.replace('\"', '\\\"')
  return '\"%s\"' % s

def current_branch():
  return filter(lambda x: x[1], all_branches())[0][0]

def all_branches():
  branches = command_lines('branch', ['-a'])
  arr = []
  for b in branches:
    current = b[0:2] == '* '
    arr.append((b[2:], current))
  return arr

def branch_exists(branch):
  return branch in map(lambda x: x[0], all_branches())

def tree(branch, recursive = False):
  opts = []
  if recursive:
    opts.append('-r')
  opts.append(branch)
  raws = command_lines('ls-tree', opts)
  objs = []
  for line in raws:
    meta, file = line.split('\t', 1)
    mode, type, sha = meta.split(' ', 2)
    objs.append((mode, type, sha, file))
  return objs

def full_tree(branch):
  return tree(branch, True)

def cat_file(sha):
  return command_lines('cat-file', [ '-p', sha ])

def change_head_branch(branch):
  return command_lines('symbolic-ref', ['HEAD', 'refs/heads/%s' % branch])

def command_lines(subcmd, opts = []):
  cmd = 'git %s %s' % (subcmd, ' '.join(map(quote_string, opts)))
  output = os.popen(cmd).read()
  if output.endswith(os.linesep):
    output = output[:-len(os.linesep)]
  return output.split(os.linesep)

if __name__ == '__main__':
  print full_tree(current_branch())
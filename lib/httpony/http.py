# --                                                            ; {{{1
#
# File        : httpony/http.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2015-03-02
#
# Copyright   : Copyright (C) 2015  Felix C. Stegerman
# Licence     : LGPLv3+
#
# --                                                            ; }}}1

from . import stream as S

# TODO
def generic_messages(si):
  """..."""
  while True:
    headers = {}
    while True:
      start_line = si.readline()
      if start_line == "": return
      if start_line != S.CRLF: break
    while True:
      line = si.readline()
      if line == "": return
      if line == S.CRLF: break
      k, v = line.split(":", 1); headers[k.lower()] = v.strip()
    yield dict(
      start_line = start_line.rstrip(S.CRLF), headers = headers,
      body = si
    )

# TODO
def split_body(msg, bufsize):
  """..."""
  cl = int(msg["headers"].get("content-length", 0))
  return msg["body"].split(cl, bufsize)

# TODO
def requests(si, bufsize = S.DEFAULT_BUFSIZE):
  """..."""
  for msg in generic_messages(si):
    method, uri, version = msg["start_line"].split(" ")
    co = msg["headers"].get("connection", "keep-alive").lower()
    body, si = split_body(msg, bufsize)
    yield dict(
      method = method, uri = uri, version = version,
      headers = msg["headers"], body = body
    )
    if co == "close":
      si.close()
      return

# TODO
def responses(si, bufsize = S.DEFAULT_BUFSIZE):
  """..."""
  for msg in generic_messages(si):
    version, status, reason = msg["start_line"].split(" ", 2)
    body, si = split_body(msg, bufsize)
    yield dict(
      version = version, status = int(status), reason = reason,
      headers = msg["headers"], body = body
    )

# TODO
def evaluate_bodies(xs):
  """..."""
  for msg in xs:
    msg["body"] = msg["body"].read()
    yield msg


# ...

# vim: set tw=70 sw=2 sts=2 et fdm=marker :

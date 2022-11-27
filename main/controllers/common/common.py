from functools import wraps
from main.models.common.error import (
    ERROR_LIST_PAGE_INVALID,
    ERROR_LIST_LENGTH_INVALID
)
import string
import random


def get_page_offset(page, length):
  return length * (page - 1)


def check_pagination_request(fn):
  """
  @check_pagination_request
  def function(page, length, **kwargs):
    SOMETHING
  """

  @wraps(fn)
  def wrapper(*args, **kwargs):
    if kwargs["page"] <= 0:
      return ERROR_LIST_PAGE_INVALID.get_response()
    if kwargs["length"] < 0:
      return ERROR_LIST_LENGTH_INVALID.get_response()

    return fn(*args, **kwargs)
  return wrapper


def convert_query_to_response(attrs, elems):
  if isinstance(elems, list):
    return [{attr: col for attr, col in zip(attrs, elem)} for elem in elems]
  else:
    return {attr: col for attr, col in zip(attrs, elems)}


def escape_wildcards(stmt, wildcards):
  for w in wildcards:
    stmt = stmt.replace(w, f"\\{w}")
  return stmt


def gen_random_uid(uid_len=22):
  available_chrs = string.ascii_uppercase + string.ascii_lowercase + string.digits + "-" + "_"
  return "".join(random.SystemRandom().choice(available_chrs) for _ in range(uid_len))

from .s3_copy import copy
from .s3_list import list_objects
from .s3_read import read, read_badpractice
from .s3_write import write
from .storage_formats import format_fn_map


supported_formats = list(format_fn_map.keys())


__all__ = [
    'copy',
    'list_objects',
    'read',
    'read_badpractice',
    'write',
    'supported_formats'
]

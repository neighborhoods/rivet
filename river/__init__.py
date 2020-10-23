from .s3_copy import copy
from .s3_delete import delete
from .s3_list import list_objects, exists
from .s3_read import read, read_badpractice
from .s3_write import write
from .storage_formats import format_fn_map


supported_formats = list(format_fn_map.keys())


__all__ = [
    'copy',
    'delete',
    'exists',
    'list_objects',
    'read',
    'read_badpractice',
    'write',
    'supported_formats'
]

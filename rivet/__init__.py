from .config import get_option, set_option
from .inform import inform
from .s3_copy import copy
from .s3_delete import delete
from .s3_list import list_objects, exists
from .s3_read import read, read_df_in_chunks, read_badpractice, download_file
from .s3_write import write, upload_file
from .storage_formats import format_fn_map
from ._version import (
    __title__, __description__, __url__, __version__,
    __author__, __author_email__)


supported_formats = list(format_fn_map.keys())


__all__ = [
    'copy',
    'delete',
    'exists',
    'list_objects',
    'read',
    'read_df_in_chunks',
    'read_badpractice',
    'download_file',
    'write',
    'upload_file',
    'supported_formats',
    'get_option',
    'set_option',
    'inform',
    '__title__',
    '__description__',
    '__url__',
    '__version__',
    '__author__',
    '__author_email__'
]

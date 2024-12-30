# cacaodocs/__init__.py

from .documentation import CacaoDocs
from .parser import DocstringParser

__all__ = ['CacaoDocs']
# Remove the redundant CacaoDocs class definition below# class CacaoDocs:#     @classmethod#     def doc_api(cls, doc_type="api", tag="general"):#         def decorator(func):#             docstring = func.__doc__ or ""#             parsed_doc = DocstringParser.parse_docstring(docstring)#             #             # Store the parsed documentation#             cls._registry.append({#                 'type': doc_type,#                 'tag': tag,#                 'name': func.__name__,#                 'doc': parsed_doc#             })#             return func#         return decorator
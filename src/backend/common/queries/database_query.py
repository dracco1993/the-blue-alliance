import abc
from typing import Any, Dict, Generic, Type

from google.cloud import ndb
from pyre_extensions import safe_cast

from backend.common.consts.api_version import ApiMajorVersion
from backend.common.futures import TypedFuture
from backend.common.profiler import Span
from backend.common.queries.dict_converters.converter_base import ConverterBase
from backend.common.queries.exceptions import DoesNotExistException
from backend.common.queries.types import QueryReturn


class DatabaseQuery(abc.ABC, Generic[QueryReturn]):
    _query_args: Dict[str, Any]
    DICT_CONVERTER: Type[ConverterBase[QueryReturn]] = ConverterBase

    def __init__(self, *args, **kwargs) -> None:
        self._query_args = kwargs

    @abc.abstractmethod
    def _query_async(self) -> TypedFuture[QueryReturn]:
        ...

    def fetch(self) -> QueryReturn:
        return self.fetch_async().get_result()

    @ndb.tasklet
    def fetch_async(self) -> TypedFuture[QueryReturn]:
        with Span("{}.fetch_async".format(self.__class__.__name__)):
            query_result = yield self._query_async(**self._query_args)
            return safe_cast(TypedFuture[QueryReturn], query_result)

    def fetch_dict(self, version: ApiMajorVersion) -> Dict:
        return self.fetch_dict_async(version).get_result()

    @ndb.tasklet
    def fetch_dict_async(self, version: ApiMajorVersion) -> TypedFuture[Dict]:
        query_result = yield self.fetch_async()
        if query_result is None:
            raise DoesNotExistException()
        # See https://github.com/facebook/pyre-check/issues/267
        res = self.DICT_CONVERTER(  # pyre-ignore[45]
            safe_cast(QueryReturn, query_result)
        ).convert(version)
        return safe_cast(TypedFuture[Dict], res)

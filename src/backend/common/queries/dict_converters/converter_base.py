import abc
from typing import Dict, Generic, List, Union

from backend.common.consts.api_version import ApiMajorVersion
from backend.common.profiler import Span
from backend.common.queries.types import QueryReturn


class ConverterBase(abc.ABC, Generic[QueryReturn]):
    _query_return: QueryReturn

    def __init__(self, query_return: QueryReturn):
        self._query_return = query_return

    def convert(self, version: ApiMajorVersion) -> Union[None, Dict, List[Dict]]:
        with Span("{}.convert".format(self.__class__.__name__)):
            converted_query_return = self._convert_list(
                self._listify(self._query_return), version
            )
            if isinstance(self._query_return, list):
                return converted_query_return
            else:
                return self._delistify(converted_query_return)

    @abc.abstractmethod
    def _convert_list(self, model_list: List, version: ApiMajorVersion) -> List[Dict]:
        return [{} for model in model_list]

    def _listify(self, thing: QueryReturn) -> List:
        if not isinstance(thing, list):
            return [thing]
        else:
            return thing

    def _delistify(self, things: List[Dict]) -> Union[None, Dict, List[Dict]]:
        if len(things) == 0:
            return None
        if len(things) == 1:
            return things.pop()
        else:
            return things

    def constructLocation_v3(self, model) -> Dict:
        """
        Works for teams and events
        """
        has_nl = (
            model.nl
            and model.nl.city
            and model.nl.state_prov_short
            and model.nl.country_short_if_usa
        )
        return {
            "city": model.nl.city if has_nl else model.city,
            "state_prov": model.nl.state_prov_short if has_nl else model.state_prov,
            "country": model.nl.country_short_if_usa if has_nl else model.country,
            "postal_code": model.nl.postal_code if has_nl else model.postalcode,
            "lat": model.nl.lat_lng.latitude if has_nl else None,
            "lng": model.nl.lat_lng.longitude if has_nl else None,
            "location_name": model.nl.name if has_nl else None,
            "address": model.nl.formatted_address if has_nl else None,
            "gmaps_place_id": model.nl.place_id if has_nl else None,
            "gmaps_url": model.nl.place_details.get("url") if has_nl else None,
        }

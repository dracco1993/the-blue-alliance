from typing import List, Optional

from google.cloud import ndb

from backend.common.futures import TypedFuture
from backend.common.models.event import Event
from backend.common.models.keys import EventKey, MatchKey, TeamKey, Year
from backend.common.models.match import Match
from backend.common.queries.database_query import DatabaseQuery
from backend.common.queries.dict_converters.match_converter import MatchConverter


class MatchQuery(DatabaseQuery[Optional[Match]]):
    DICT_CONVERTER = MatchConverter

    @ndb.tasklet
    def _query_async(self, match_key: MatchKey) -> TypedFuture[Optional[Match]]:
        match = yield Match.get_by_id_async(match_key)
        return match


class EventMatchesQuery(DatabaseQuery[List[Match]]):
    DICT_CONVERTER = MatchConverter

    @ndb.tasklet
    def _query_async(self, event_key: EventKey):
        match_keys = yield Match.query(
            Match.event == ndb.Key(Event, event_key)
        ).fetch_async(keys_only=True)
        matches = yield ndb.get_multi_async(match_keys)
        return list(filter(None, matches))


class TeamEventMatchesQuery(DatabaseQuery[List[Match]]):
    DICT_CONVERTER = MatchConverter

    @ndb.tasklet
    def _query_async(self, team_key: TeamKey, event_key: EventKey) -> List[Match]:
        match_keys = yield Match.query(
            Match.team_key_names == team_key, Match.event == ndb.Key(Event, event_key)
        ).fetch_async(keys_only=True)
        matches = yield ndb.get_multi_async(match_keys)
        return list(filter(None, matches))


class TeamYearMatchesQuery(DatabaseQuery[List[Match]]):
    DICT_CONVERTER = MatchConverter

    @ndb.tasklet
    def _query_async(self, team_key: TeamKey, year: Year) -> List[Match]:
        match_keys = yield Match.query(
            Match.team_key_names == team_key, Match.year == year
        ).fetch_async(keys_only=True)
        matches = yield ndb.get_multi_async(match_keys)
        return list(filter(None, matches))

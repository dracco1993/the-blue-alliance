import json

from google.cloud import ndb

from backend.common.consts.suggestion_state import SuggestionState
from backend.common.consts.suggestion_type import SUGGESTION_TYPES
from backend.common.models.account import Account


class Suggestion(ndb.Model):
    """
    Suggestions are generic containers for user-submitted data corrections to
    the site. The generally store a model, a key, and then a json blob of
    fields to append or ammend in the model.
    """

    # social-media is a Media with no year
    # offseason-event is for new events (opposed to 'event' for adding webcasts to existing events)

    review_state = ndb.IntegerProperty(
        default=SuggestionState.REVIEW_PENDING, choices=list(SuggestionState)
    )
    reviewed_at = ndb.DateTimeProperty()
    reviewer = ndb.KeyProperty(kind=Account)
    author = ndb.KeyProperty(kind=Account, required=True)
    contents_json = ndb.TextProperty(indexed=False)  # a json blob
    target_key = ndb.StringProperty()  # "2012cmp"
    target_model = ndb.StringProperty(choices=set(SUGGESTION_TYPES), required=True)

    created = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    updated = ndb.DateTimeProperty(auto_now=True, indexed=False)

    def __init__(self, *args, **kw):
        self._contents = None
        super(Suggestion, self).__init__(*args, **kw)

    def put(self, *args, **kwargs):
        if self.review_state == SuggestionState.REVIEW_PENDING:
            user = self.author.get()
            if user and user.shadow_banned:
                self.review_state = SuggestionState.REVIEW_AUTOREJECTED
        return super(Suggestion, self).put(*args, **kwargs)

    @property
    def contents(self):
        """
        Lazy load contents_json
        """
        if self._contents is None:
            self._contents = json.loads(self.contents_json)
        return self._contents

    @contents.setter
    def contents(self, contents):
        self._contents = contents
        self.contents_json = json.dumps(self._contents)

    # @property
    # def candidate_media(self):
    #     team_reference = Media.create_reference(
    #         self.contents['reference_type'],
    #         self.contents['reference_key'])
    #     return MediaCreator.create_media_model(self, team_reference)
    #
    # @property
    # def youtube_video(self):
    #     if "youtube_videos" in self.contents:
    #         return self.contents["youtube_videos"][0]
    #
    # @classmethod
    # def render_media_key_name(cls, year, target_model, target_key, foreign_type, foreign_key):
    #     """
    #     Keys aren't required for this model. This is only necessary if checking
    #     for duplicate suggestions is desired.
    #     """
    #     return 'media_{}_{}_{}_{}_{}'.format(year, target_model, target_key, foreign_type, foreign_key)
    #
    # @classmethod
    # def render_webcast_key_name(cls, event_key, webcast_dict):
    #     """
    #     Keys aren't required for this model. This is only necessary if checking
    #     for duplicate suggestions is desired.
    #     """
    #     return 'webcast_{}_{}_{}_{}'.format(
    #         event_key,
    #         webcast_dict.get('type', None),
    #         webcast_dict.get('channel', None),
    #         webcast_dict.get('file', None))

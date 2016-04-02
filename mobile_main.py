import endpoints
import json
import logging

from google.appengine.ext import ndb

from protorpc import remote
from protorpc import message_types

import tba_config

from consts.client_type import ClientType
from helpers.media_helper import MediaParser
from helpers.push_helper import PushHelper
from helpers.mytba_helper import MyTBAHelper
from helpers.suggestions.suggestion_creator import SuggestionCreator
from helpers.youtube_video_helper import YouTubeVideoHelper
from models.account import Account
from models.event import Event
from models.favorite import Favorite
from models.match import Match
from models.media import Media
from models.sitevar import Sitevar
from models.subscription import Subscription
from models.mobile_api_messages import BaseResponse, FavoriteCollection, FavoriteMessage, RegistrationRequest, \
                                       SubscriptionCollection, SubscriptionMessage, ModelPreferenceMessage, \
                                       MediaSuggestionMessage, MediaSuggestionCollection
from models.mobile_client import MobileClient
from models.suggestion import Suggestion

client_id_sitevar = Sitevar.get_by_id('appengine.webClientId')
if client_id_sitevar is None:
    raise Exception("Sitevar appengine.webClientId is undefined. Can't process incoming requests")
WEB_CLIENT_ID = str(client_id_sitevar.values_json)
ANDROID_AUDIENCE = WEB_CLIENT_ID

android_id_sitevar = Sitevar.get_by_id('android.clientId')
if android_id_sitevar is None:
    raise Exception("Sitevar android.clientId is undefined. Can't process incoming requests")
ANDROID_CLIENT_ID = str(android_id_sitevar.values_json)

# To enable iOS access to the API, add another variable for the iOS client ID

client_ids = [WEB_CLIENT_ID, ANDROID_CLIENT_ID]
if tba_config.DEBUG:
    '''
    Only allow API Explorer access on dev versions
    '''
    client_ids.append(endpoints.API_EXPLORER_CLIENT_ID)

# To enable iOS access, add it's client ID here


@endpoints.api(name='tbaMobile', version='v9', description="API for TBA Mobile clients",
               allowed_client_ids=client_ids,
               audiences=[ANDROID_AUDIENCE],
               scopes=[endpoints.EMAIL_SCOPE])
class MobileAPI(remote.Service):

    @endpoints.method(RegistrationRequest, BaseResponse,
                      path='register', http_method='POST',
                      name='register')
    def register_client(self, request):
        current_user = endpoints.get_current_user()
        if current_user is None:
            return BaseResponse(code=401, message="Unauthorized to register")
        user_id = PushHelper.user_email_to_id(current_user.email())
        gcm_id = request.mobile_id
        os = ClientType.enums[request.operating_system]
        name = request.name
        uuid = request.device_uuid

        query = MobileClient.query(
                MobileClient.user_id == user_id,
                MobileClient.device_uuid == uuid,
                MobileClient.client_type == os)
        # trying to figure out an elusive dupe bug
        logging.info("DEBUGGING")
        logging.info("User ID: {}".format(user_id))
        logging.info("UUID: {}".format(uuid))
        logging.info("Count: {}".format(query.count()))
        if query.count() == 0:
            # Record doesn't exist yet, so add it
            MobileClient(
                parent=ndb.Key(Account, user_id),
                user_id=user_id,
                messaging_id=gcm_id,
                client_type=os,
                device_uuid=uuid,
                display_name=name).put()
            return BaseResponse(code=200, message="Registration successful")
        else:
            # Record already exists, update it
            client = query.fetch(1)[0]
            client.messaging_id = gcm_id
            client.display_name = name
            client.put()
            return BaseResponse(code=304, message="Client already exists")

    @endpoints.method(RegistrationRequest, BaseResponse,
                      path='unregister', http_method='POST',
                      name='unregister')
    def unregister_client(self, request):
        current_user = endpoints.get_current_user()
        if current_user is None:
            return BaseResponse(code=401, message="Unauthorized to unregister")
        user_id = PushHelper.user_email_to_id(current_user.email())
        gcm_id = request.mobile_id
        query = MobileClient.query(MobileClient.messaging_id == gcm_id, ancestor=ndb.Key(Account, user_id))\
            .fetch(keys_only=True)
        if len(query) == 0:
            # Record doesn't exist, so we can't remove it
            return BaseResponse(code=404, message="User doesn't exist. Can't remove it")
        else:
            ndb.delete_multi(query)
            return BaseResponse(code=200, message="User deleted")

    @endpoints.method(message_types.VoidMessage, FavoriteCollection,
                      path='favorites/list', http_method='POST',
                      name='favorites.list')
    def list_favorites(self, request):
        current_user = endpoints.get_current_user()
        if current_user is None:
            return FavoriteCollection(favorites=[])
        user_id = PushHelper.user_email_to_id(current_user.email())

        favorites = Favorite.query(ancestor=ndb.Key(Account, user_id)).fetch()
        output = []
        for favorite in favorites:
            output.append(FavoriteMessage(model_key=favorite.model_key, model_type=favorite.model_type))
        return FavoriteCollection(favorites=output)

    @endpoints.method(ModelPreferenceMessage, BaseResponse,
                      path="model/setPreferences", http_method="POST",
                      name="model.setPreferences")
    def update_model_preferences(self, request):
        current_user = endpoints.get_current_user()
        if current_user is None:
            return BaseResponse(code=401, message="Unauthorized to update model preferences")
        user_id = PushHelper.user_email_to_id(current_user.email())
        model_key = request.model_key
        output = {}
        code = 0

        if request.favorite:
            fav = Favorite(
                parent=ndb.Key(Account, user_id),
                user_id=user_id,
                model_key=model_key,
                model_type=request.model_type
            )
            result = MyTBAHelper.add_favorite(fav, request.device_key)
            if result == 200:
                output['favorite'] = {"code":    200,
                                      "message": "Favorite added"}
                code += 100
            elif result == 304:
                output['favorite'] = {"code":    304,
                                      "message": "Favorite already exists"}
                code += 304
            else:
                output['favorite'] = {"code":    500,
                                      "message": "Unknown error adding favorite"}
                code += 500
        else:
            result = MyTBAHelper.remove_favorite(user_id, model_key, request.device_key)
            if result == 200:
                output['favorite'] = {"code":    200,
                                      "message": "Favorite deleted"}
                code += 100
            elif result == 404:
                output['favorite'] = {"code":    404,
                                      "message": "Favorite not found"}
                code += 404
            else:
                output['favorite'] = {"code":    500,
                                      "message": "Unknown error removing favorite"}
                code += 500

        if request.notifications:
            sub = Subscription(
                parent=ndb.Key(Account, user_id),
                user_id=user_id,
                model_key=model_key,
                model_type=request.model_type,
                notification_types=PushHelper.notification_enums_from_string(request.notifications)
            )
            result = MyTBAHelper.add_subscription(sub, request.device_key)
            if result == 200:
                output['subscription'] = {"code":    200,
                                          "message": "Subscription updated"}
                code += 100
            elif result == 304:
                output['subscription'] = {"code":    304,
                                          "message": "Subscription already exists"}
                code += 304
            else:
                output['subscription'] = {"code":    500,
                                          "message": "Unknown error adding favorite"}
                code += 500
        else:
            result = MyTBAHelper.remove_subscription(user_id, model_key, request.device_key)
            if result == 200:
                output['subscription'] = {"code":    200,
                                          "message": "Subscription removed"}
                code += 100
            elif result == 404:
                output['subscription'] = {"code":    404,
                                          "message": "Subscription not found"}
                code += 404
            else:
                output['subscription'] = {"code":    500,
                                          "message": "Unknown error removing subscription"}
                code += 500

        return BaseResponse(code=code, message=json.dumps(output))

    @endpoints.method(message_types.VoidMessage, SubscriptionCollection,
                      path='subscriptions/list', http_method='POST',
                      name='subscriptions.list')
    def list_subscriptions(self, request):
        current_user = endpoints.get_current_user()
        if current_user is None:
            return SubscriptionCollection(subscriptions=[])
        user_id = PushHelper.user_email_to_id(current_user.email())

        subscriptions = Subscription.query(ancestor=ndb.Key(Account, user_id)).fetch()
        output = []
        for subscription in subscriptions:
            output.append(SubscriptionMessage(
                    model_key=subscription.model_key,
                    notifications=PushHelper.notification_string_from_enums(subscription.notification_types),
                    model_type=subscription.model_type))
        return SubscriptionCollection(subscriptions=output)

    @endpoints.method(MediaSuggestionMessage, BaseResponse,
                      path='team/media/suggest', http_method='POST',
                      name='team.media.suggestion')
    def suggest_team_media(self, request):
        current_user = endpoints.get_current_user()
        if current_user is None:
            return BaseResponse(code=401, message="Unauthorized to make suggestions")
        user_id = PushHelper.user_email_to_id(current_user.email())

        # For now, only allow team media suggestions
        if request.reference_type != "team":
            # Trying to suggest a media for an invalid model type
            return BaseResponse(code=400, message="Bad model type")

        # Need to split deletehash out into its own private dict. Don't want that to be exposed via API...
        private_details_json = None
        if request.details_json:
            incoming_details = json.loads(request.details_json)
            private_details = None
            if 'deletehash' in incoming_details:
                private_details = {'deletehash': incoming_details.pop('deletehash')}
            private_details_json = json.dumps(private_details) if private_details else None

        status = SuggestionCreator.createTeamMediaSuggestion(
            author_account_key=ndb.Key(Account, user_id),
            media_url=request.media_url,
            team_key=request.reference_key,
            year_str=str(request.year),
            private_details_json=private_details_json)

        if status != 'bad_url':
            if status == 'success':
                return BaseResponse(code=200, message="Suggestion added")
            else:
                return BaseResponse(code=304, message="Suggestion already exists")
        else:
            return BaseResponse(code=400, message="Bad suggestion url")

    @endpoints.method(MediaSuggestionCollection, BaseResponse,
                      path='match/videos/suggest', http_method='POST',
                      name='match.videos.suggestion')
    def suggest_event_match_videos(self, request):
        current_user = endpoints.get_current_user()
        if current_user is None:
            return BaseResponse(code=401, message="Unauthorized to make suggestions")
        user_id = PushHelper.user_email_to_id(current_user.email())

        event_key = request.reference_key
        event = Event.get_by_id(event_key)
        if event is None:
            return BaseResponse(code=404, message="Event {} not found".format(event_key))

        match_futures = Match.query(Match.event == event.key).fetch_async(keys_only=True)
        valid_match_keys = [match.id() for match in match_futures.get_result()]
        bad_match_keys = []
        success_keys = []

        for suggestion in request.suggestions:
            if "match" != suggestion.reference_type:
                continue

            match_key = "{}_{}".format(event_key, suggestion.reference_key)
            if match_key not in valid_match_keys:
                bad_match_keys.append(match_key)
                continue

            youtube_id = YouTubeVideoHelper.parse_id_from_url(suggestion.media_url)
            status = SuggestionCreator.createMatchVideoYouTubeSuggestion(
                author_account_key=ndb.Key(Account, user_id),
                youtube_id=youtube_id,
                match_key=match_key)
            if status == 'success':
                success_keys.append(match_key)

        return BaseResponse(code=200, message="Added suggestions for {} and skipped bad keys {}".format(json.dumps(success_keys), json.dumps(bad_match_keys)))


app = endpoints.api_server([MobileAPI])

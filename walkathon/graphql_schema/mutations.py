import graphene
from graphql import GraphQLError

from .types import WalkerType, StreamingType, UserType
from ..helpers.common import handle_model_update
from ..helpers.common import iso_string_to_datetime
from ..helpers.graphql_helpers import send_password_reset_message, send_contact_us_message
from ..helpers.walker import WalkerHelper
from ..models import Walker, Streaming


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        if not username or not password:
            raise GraphQLError('Enter valid username and password')

        user = WalkerHelper(username, password).create_new_walker()
        return CreateUser(user=user)


class ResetPassword(graphene.Mutation):
    response = graphene.String()

    class Arguments:
        username = graphene.String(required=True)

    def mutate(self, info, username):
        return ResetPassword(send_password_reset_message(username))


class StreamInput(graphene.InputObjectType):
    stream_key = graphene.String()
    year = graphene.Int()
    mux_token_id = graphene.String()
    mux_token_secret = graphene.String()
    playback_id = graphene.String()
    stream_id = graphene.String()
    stream_started = graphene.Boolean()
    stream_ended = graphene.Boolean()


class UpdateOrCreateStream(graphene.Mutation):
    class Arguments:
        stream_input = StreamInput(required=True)

    stream = graphene.Field(StreamingType)

    def mutate(self, info, stream_input):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to create a walker profile!')

        Streaming.objects.update_or_create(
            stream_id=stream_input.stream_id, created_by=user_profile, defaults={**stream_input})
        stream, created = Streaming.objects.filter(
            created_by=user_profile, stream_id=stream_input.stream_id).first()
        handle_model_update('streams')
        return UpdateOrCreateStream(stream)


class WalkerInput(graphene.InputObjectType):
    fcm_token = graphene.String()
    distance_to_walk = graphene.String()
    total_walked_distance = graphene.String()
    walk_method = graphene.String()
    device_type = graphene.String()
    steps_walked = graphene.String()
    time_started = graphene.String()
    time_ended = graphene.String()
    milestones = graphene.String()
    messages_read = graphene.String()
    messages_received = graphene.String()
    route_coordinates = graphene.String()


class UpdateWalker(graphene.Mutation):
    class Arguments:
        walker_input = WalkerInput(required=True)

    walker = graphene.Field(WalkerType)

    def mutate(self, info, walker_input):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to create a walker profile!')
        if walker_input.time_ended:
            walker_input['time_ended'] = iso_string_to_datetime(walker_input.time_ended)
        if walker_input.time_started:
            walker_input['time_started'] = iso_string_to_datetime(walker_input.time_started)

        Walker.objects.filter(user_profile=user_profile).update(**walker_input)
        walker = Walker.objects.filter(user_profile=user_profile).first()
        return UpdateWalker(walker)


class ContactUsInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    contact = graphene.String(required=True)
    message = graphene.String(required=True)


class IncomingContactUsMessage(graphene.Mutation):
    class Arguments:
        contact_us_input = ContactUsInput(required=True)

    feedback = graphene.String()

    def mutate(self, info, contact_us_input):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to create a walker profile!')
        send_contact_us_message(user_profile, contact_us_input)
        return IncomingContactUsMessage('done')


class Mutation(graphene.ObjectType):
    update_walker = UpdateWalker.Field()
    update_or_create_stream = UpdateOrCreateStream.Field()
    create_user = CreateUser.Field()
    incoming_contact_us_message = IncomingContactUsMessage.Field()
    reset_password = ResetPassword.Field()

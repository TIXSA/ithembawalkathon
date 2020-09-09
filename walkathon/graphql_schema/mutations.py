import graphene
from graphql import GraphQLError
from django.contrib.auth import get_user_model


from ..helpers.streaming import handle_stream_update_or_create
from ..models import Walker, Streaming
from .types import WalkerType, StreamingType, UserType


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        if not username or not password:
            raise GraphQLError('Enter valid username and password')
        user = get_user_model()(
            username=username,
            password=password,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


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
        handle_stream_update_or_create(stream)
        return UpdateOrCreateStream(stream)


class WalkerInput(graphene.InputObjectType):
    fcm_token = graphene.String()
    distance_to_walk = graphene.String()
    total_walked_distance = graphene.Int()
    walk_method = graphene.String()
    device_type = graphene.String()
    steps_walked = graphene.String()
    time_started = graphene.String()
    time_ended = graphene.String()
    milestones = graphene.String()
    messages_read = graphene.String()
    messages_received = graphene.String()


class UpdateWalker(graphene.Mutation):
    class Arguments:
        walker_input = WalkerInput(required=True)

    walker = graphene.Field(WalkerType)

    def mutate(self, info, walker_input):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to create a walker profile!')
        Walker.objects.filter(user_profile=user_profile).update(**walker_input)
        walker = Walker.objects.filter(user_profile=user_profile).first()
        return UpdateWalker(walker)


class Mutation(graphene.ObjectType):
    update_walker = UpdateWalker.Field()
    update_or_create_stream = UpdateOrCreateStream.Field()
    create_user = CreateUser.Field()

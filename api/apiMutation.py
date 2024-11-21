from api.apiQuery import *
from api.apiAuth import enrolAppUser, authenticateAppUser, RefreshMutation


class Mutation(graphene.ObjectType):
    authenticate_app_user           = authenticateAppUser.Field()
    enrol_app_user                  = enrolAppUser.Field()

    refresh_mutation                = RefreshMutation.Field()






schema_query    = graphene.Schema(query=Query)#, type=[EnrolmentObject])
schema_mutation = graphene.Schema(query=Query, mutation=Mutation)
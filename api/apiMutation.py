from api.apiQuery import *
from api.apiAuth import activateAppUser, deactivateAppUser, enrolAppUser, authenticateAppUser, refreshMutation, validateAppUser
from api.student_records import addStudentData


class Mutation(graphene.ObjectType):
    enrol_app_user                  = enrolAppUser.Field()

    authenticate_app_user           = authenticateAppUser.Field()
    refresh_mutation                = refreshMutation.Field()

    activate_app_user               = activateAppUser.Field()
    deactivate_app_user             = deactivateAppUser.Field()
    validate_app_user               = validateAppUser.Field()

    add_student_data                = addStudentData.Field()
    






schema_query    = graphene.Schema(query=Query)#, type=[EnrolmentObject])
schema_mutation = graphene.Schema(query=Query, mutation=Mutation)
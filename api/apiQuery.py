import json
import math
from decimal import Decimal, ROUND_UP
import time
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_, and_
from api.filters import Userfilter
from app import db

from flask_graphql_auth import (
    AuthInfoField,
    GraphQLAuth,
    get_jwt_identity,
    get_raw_jwt,
    create_access_token,
    create_refresh_token,
    query_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required,
)
from helpers import confirmEmail

from app.models import User, Student

from app.models import User as UserModel
from app.models import Student as StudentModel

class UserObject(SQLAlchemyObjectType):
    class Meta:
        model           = UserModel
        interfaces      = (graphene.relay.Node,)

class StudentObject(SQLAlchemyObjectType):
    class Meta:
        model           = StudentModel
        interfaces      = (graphene.relay.Node,)

class enrolmentAppUserInput(graphene.InputObjectType):
    email                   = graphene.String()
    password                = graphene.String()
    password_confirm        = graphene.String()

class studentDataInput(graphene.InputObjectType):
    first_name      = graphene.String(required=True)
    middle_name     = graphene.String()
    last_name       = graphene.String(required=True)
    date_of_birth   = graphene.String(required=True)  # Should be in 'YYYY-MM-DD' format
    gender          = graphene.String(required=True)
    matric_number   = graphene.String(required=True)
    email           = graphene.String(required=True)
    phone_number    = graphene.String(required=True)
    address         = graphene.String()
    department      = graphene.String(required=True)
    enrollment_year = graphene.Int(required=True)
    current_gpa     = graphene.Float()
        

class authenticateAppUserInput(graphene.InputObjectType):
    email                   = graphene.String()
    password                = graphene.String()

class Query(graphene.ObjectType):
    ''' We can set the schema description for an Object Type here on a docstring '''
    node                                = graphene.relay.Node.Field()

    all_users                           = SQLAlchemyConnectionField(UserObject.connection,
                                                                    filters=Userfilter(),
                                                                      token=graphene.String(required=True)
                                                                    )
    @query_jwt_required
    def resolve_all_users(self, info, **args): 
        allusers        = UserObject.get_query(info)
        return allusers
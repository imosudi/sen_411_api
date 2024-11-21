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

from app.models import User 

from app.models import User as UserModel

class UserObject(SQLAlchemyObjectType):
    class Meta:
        model           = UserModel
        interfaces      = (graphene.relay.Node,)


class enrolmentAppUserInput(graphene.InputObjectType):
    email                   = graphene.String()
    password                = graphene.String()
    password_confirm        = graphene.String()


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
        #allusers        = allusers.filter(UserModel.email=="imosudi@gmail.com").all()
        return allusers
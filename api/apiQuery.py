import json
import math
from decimal import Decimal, ROUND_UP
import time
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_, and_
from api.filters import Studentfilter, Userfilter
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
    
    user_by_email                           = SQLAlchemyConnectionField(UserObject.connection,
                                                                    filters=Userfilter(),
                                                                      email=graphene.String(required=True),
                                                                      token=graphene.String(required=True)
                                                                    )
    @query_jwt_required
    def resolve_user_by_email(self, info, email, **args): 
        allusers        = UserObject.get_query(info)
        theuser         = allusers.filter(UserModel.email==email)#.first()
        return theuser
    
    all_student_record                           = SQLAlchemyConnectionField(StudentObject.connection,
                                                                    filters=Studentfilter(),
                                                                      token=graphene.String(required=True)
                                                                    )
    @query_jwt_required
    def resolve_all_student_record(self, info, **args): 
        all_students        = StudentObject.get_query(info)
        return all_students
    
    student_record_by_email                           = SQLAlchemyConnectionField(StudentObject.connection,
                                                                    filters=Studentfilter(),
                                                                      email=graphene.String(required=True),
                                                                      token=graphene.String(required=True)
                                                                    )
    @query_jwt_required
    def resolve_student_record_by_email(self, info, email, **args): 
        all_students        = StudentObject.get_query(info)
        thestudent         = all_students.filter(StudentModel.email==email)#.first()
        return thestudent
    
    student_record_by_matric                           = SQLAlchemyConnectionField(StudentObject.connection,
                                                                    filters=Studentfilter(),
                                                                      matric=graphene.String(required=True),
                                                                      token=graphene.String(required=True)
                                                                    )
    @query_jwt_required
    def resolve_student_record_by_matric(self, info, matric, **args): 
        all_students        = StudentObject.get_query(info)
        thestudent         = all_students.filter(StudentModel.matric_number==matric)#.first()
        return thestudent
    
    student_record_by_email_matric                           = SQLAlchemyConnectionField(StudentObject.connection,
                                                                    filters=Studentfilter(),
                                                                      email=graphene.String(required=True),
                                                                      matric=graphene.String(required=True),
                                                                      token=graphene.String(required=True)
                                                                    )
    @query_jwt_required
    def resolve_student_record_by_email_matric(self, info, email, matric, **args): 
        all_students        = StudentObject.get_query(info)
        thestudent         = all_students.filter(and_(StudentModel.matric_number==matric, StudentModel.email==email))#.first()
        return thestudent

    
    students_record_by_department                          = SQLAlchemyConnectionField(StudentObject.connection,
                                                                    filters=Studentfilter(),
                                                                      department=graphene.String(required=True),
                                                                      token=graphene.String(required=True)
                                                                    )
    @query_jwt_required
    def resolve_students_record_by_department(self, info, department, **args): 
        all_students        = StudentObject.get_query(info)
        thestudents          = all_students.filter(StudentModel.department==department)#.first()
        return thestudents
    
    students_record_by_faculty                          = SQLAlchemyConnectionField(StudentObject.connection,
                                                                    filters=Studentfilter(),
                                                                      faculty=graphene.String(required=True),
                                                                      token=graphene.String(required=True)
                                                                    )
    @query_jwt_required
    def resolve_students_record_by_faculty(self, info, faculty, **args): 
        all_students        = StudentObject.get_query(info)
        thestudents          = all_students.filter(StudentModel.faculty==faculty)#.first()
        return thestudents
    

    students_record_by_level                          = SQLAlchemyConnectionField(StudentObject.connection,
                                                                    filters=Studentfilter(),
                                                                      level=graphene.Int(required=True),
                                                                      token=graphene.String(required=True)
                                                                    )
    @query_jwt_required
    def resolve_students_record_by_level(self, info, level, **args): 
        all_students        = StudentObject.get_query(info)
        thestudents          = all_students.filter(StudentModel.level==level)#.first()
        return thestudents
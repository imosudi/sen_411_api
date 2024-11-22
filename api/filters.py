from graphene_sqlalchemy_filter import FilterSet


from app.models import * 

#ALL_OPERATIONS = ['eq', 'ne', 'like', 'ilike', 'is_null', 'in', 'not_in', 'lt', 'lte', 'gt', 'gte', 'range']

 
ALL_OPERATIONS = ['contains','eq', 'ne', 'like', 'ilike', 'is_null', 'in', 'not_in', 'lt', 'lte', 'gt', 'gte', 'range']

class Userfilter(FilterSet):
    class Meta:
        model   = User
        fields  = {
            'email': ALL_OPERATIONS,
            'active': ALL_OPERATIONS,
            'login_count': ALL_OPERATIONS,
        }


class Studentfilter(FilterSet):
    class Meta:
        model   = Student
        fields  = {
            'first_name': ALL_OPERATIONS,
            'middle_name': ALL_OPERATIONS,
            'last_name': ALL_OPERATIONS,
            'date_of_birth': ALL_OPERATIONS,
            'gender': ALL_OPERATIONS,
            'matric_number': ALL_OPERATIONS,
            'email': ALL_OPERATIONS,
            'phone_number': ALL_OPERATIONS,
            'address': ALL_OPERATIONS,
            'department': ALL_OPERATIONS,
            'enrollment_year': ALL_OPERATIONS,
            'current_gpa': ALL_OPERATIONS,
            'is_active': ALL_OPERATIONS,
        }
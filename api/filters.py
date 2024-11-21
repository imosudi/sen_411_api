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
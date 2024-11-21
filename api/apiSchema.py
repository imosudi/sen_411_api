from flask_graphql import GraphQLView
from app import app

from . apiMutation import *

app.add_url_rule(
    '/api_query',
      view_func=GraphQLView.as_view(
          'graphql_query',
            schema=schema_query,
              graphiql=True
          )
        )

app.add_url_rule(
    '/api_mutation',
      view_func=GraphQLView.as_view(
          'graphql_mutation',
            schema=schema_mutation,
              graphiql=True
          )
        )

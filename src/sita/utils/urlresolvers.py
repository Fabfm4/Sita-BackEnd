# -*- coding: utf-8 -*-
import urllib

from django.core.urlresolvers import reverse


def reverse_with_querystrings(
        viewname, urlconf=None, args=None, kwargs=None,
        current_app=None, query_params=None
):
    url = '{base_url}?{query_params}'.format(
        base_url=reverse(
            viewname, urlconf=urlconf, args=args,
            kwargs=kwargs, current_app=current_app
        ),
        query_params=urllib.urlencode(query_params)
    )

    return url


def get_query_params(request):
    query_params = {}

    for key, value in request.query_params.iteritems():
        if value.lower() == 'true':
            query_params[key] = True
        elif value.lower() == "false":
            query_params[key] = False
        else:
            query_params[key] = value

    return query_params

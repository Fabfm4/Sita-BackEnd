# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.cache import cache

cache_key_format_string = '{0}::{1}::{2}'


def save_to_cache(
    group_key='',
    prefix_key='',
    identifier_key='',
    info=None,
    timeout=60  # seconds
):
    """
    Saves the information of the API into a cache key.

    - group_key:
    Keyword that belongs to the viewset class, for example
    "FilteredAreasViewSet", but obviously the word "ViewSet"
    is not needed, so we will omit it. Aplying snakecase to it, so that would
    be "filtered_areas".

    - prefix_key:
    Key word corresponding to the method inside the ViewSet, "list", for
    example.

    - identifier_key:
    Unique name used for storing and retrieving the data from the cache, for
    lists the value should be "many".

    - info:
    Information that will be stored.

    - timeout:
    Default time to expire the cached data.
    """
    cache_key = cache_key_format_string.format(
        group_key,
        prefix_key,
        identifier_key
    )
    cache.set(cache_key, info, timeout)
    return cache_key


def get_from_cache(group_key='', prefix_key='', identifier_key=''):
    """
    Retrieves information from the cache using a key.
    """
    cache_key = cache_key_format_string.format(
        group_key,
        prefix_key,
        identifier_key
    )
    cached_info = cache.get(cache_key)
    return cached_info


def remove_from_cache(group_key='', prefix_key='', identifier_key=''):
    """
    Removes cache information from the cache using a key.
    """
    cache_key = cache_key_format_string.format(
        group_key,
        prefix_key,
        identifier_key
    )

    cache.delete(cache_key)


def get_query_params_keys(query_params):
    """
    Retrieves query params as a string to be part of the identifier key.
    """
    keys = '::qp:'
    for key, value in query_params.iteritems():
        keys += '::{0}:{1}'.format(key, value)

    return keys


def get_kwargs_keys(kwargs):
    """
    Retrieves kwargs as a string to be part of the identifier key.
    """
    keys = '::kw'
    for key, value in kwargs.iteritems():
        keys += '::{0}:{1}'.format(key, value)

    return keys


def get_complete_identifier_key(
    request,
    identifier_key,
    kwargs_keys,
    query_params_keys,
    unique_by_user
):
    complete_id_key = identifier_key + kwargs_keys + query_params_keys

    if unique_by_user:
        complete_id_key += "::ru:{}".format(request.user.id)

    return complete_id_key


def get_cache_expiration_time(time=43200):
    """
    Returns the time of cache expiration, if the project is running in local
    environment, then, the cache will expirate in 1 seg, else, it will expirate
    in default time (43200 seg) or in the given time.
    """
    if settings.DEBUG:
        return 1
    return time

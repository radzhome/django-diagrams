# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.template.loader import get_template

from ..jsplumber import css_url, jsplumb_url, jquery_url, jsplumb_settings_script

register = template.Library()


@register.simple_tag
def jsplumb_jquery_url():
    return jquery_url()


@register.simple_tag
def jsplumb_javascript_url():
    return jsplumb_url()


@register.simple_tag
def jsplumb_css_url():
    return css_url()


@register.simple_tag
def jsplumb_css():
    """
    Return HTML for jsplumb CSS
    Adjust url in settings. If no url is returned, we don't want this statement to return any HTML.
    This is intended behavior.
    """
    url = jsplumb_css_url()
    if url:  # http://mothereff.in/unquoted-attributes
        return '<link href="{url}" rel=stylesheet media=screen>'.format(url=url)

@register.simple_tag
def jsplumb_settings():
    js = jsplumb_settings_script()
    if js:
        return js

@register.simple_tag
def jsplumb_javascript(jquery=False):
    """
    Return HTML for jsplumb JavaScript
    Adjust url in settings. If no url is returned, we don't want this statement to return any HTML.
    This is intended behavior.
    """
    javascript = ''

    if jquery:
        url = jsplumb_jquery_url()
        if url:
            javascript += '<script src="{url}"></script>'.format(url=url)
    url = jsplumb_javascript_url()

    if url:
        javascript += '<script src="{url}"></script>'.format(url=url)

    return javascript


@register.simple_tag(takes_context=True)
def jsplumb_select_drawing(context, *args, **kwargs):  # Context passes in all the variables
    """
    Show django.contrib.messages Messages in jsplumb alert containers
    """
    return get_template('jsplumber/select_drawing.html').render(context)


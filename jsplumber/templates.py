# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.template import Variable, VariableDoesNotExist
from django.template.base import FilterExpression, kwarg_re, TemplateSyntaxError
from django.shortcuts import render


"""
Extra features for template file handling
"""

# handle var, parse something...
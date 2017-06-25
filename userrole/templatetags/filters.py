# -*- coding: utf-8 -*-
# from builtins import ValueError

from django.template import Library
from django import template

register = Library()


@register.filter
def activeness(is_active):
    if is_active:
        return "Active"
    return "In-Active"


@register.filter
def alter_status(is_active):
    if is_active:
        return "Deactivate"
    return "Activate"


USURPERS = {
    'office_head': ['Office Head', 'Admin Assistant', 'Super Admin'],
    'officer': ['Information Officer', 'Office Head', 'Admin Assistant', 'Super Admin'],
    'office': ['Information Officer', 'Office Head',],
    'assistant': ['Admin Assistant', 'Super Admin'],
    'admin': ['Super Admin'],
}



@register.tag
def ifrole(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, role = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly two arguments" % token.contents.split()[0]
        )
    if not (role[0] == role[-1] and role[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )
    nodelist = parser.parse('endrole', )
    parser.delete_first_token()
    return RoleInGroup(role[1:-1], nodelist)


class RoleInGroup(template.Node):
    def __init__(self, role, nodelist):
        self.role = role
        self.nodelist = nodelist

    def render(self, context):
        request = context['request']
        if request.role and request.role.group.name in USURPERS[self.role]:
            return self.nodelist.render(context)
        else:
            return ''

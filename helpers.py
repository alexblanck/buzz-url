import os
import sys
import webapp2
import jinja2
import json

sys.path.insert(0, 'lib')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def render_template(template_name, template_values):
    template = JINJA_ENVIRONMENT.get_template(template_name)
    return template.render(template_values)

def write_template(request_handler, template_name, template_values):
    template_string = render_template(template_name, template_values)
    request_handler.response.write(template_string)

def write_json(request_handler, object_to_write):
    request_handler.response.headers['Content-Type'] = 'application/json'
    if request_handler.request.get("pretty", default_value=None) is not None:
        indent = 4
    else:
        indent = None
    json_string = json.dumps(object_to_write, indent=indent)
    request_handler.response.write(json_string)

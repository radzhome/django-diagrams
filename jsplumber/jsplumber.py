from __future__ import unicode_literals

from django.conf import settings

from django.templatetags.static import static

# Default settings
JSPLUMB_DEFAULTS = {
    'jquery_url': 'http://code.jquery.com/jquery.min.js',
    'jsplumb_url': 'http://jsplumbtoolkit.com/demo/js/jquery.jsPlumb-1.5.5-min.js',
    'css_url': static('jsplumber/css/jsplumber.css'),
    'draggable': True,  # jsPlumb.draggable($(".window")); use element_class here
    'element_class': '_jsplumber_element',
    'render_mode': 'jsPlumb.SVG'  # jsPlumb.setRenderMode(jsPlumb.SVG);
}

# Start with a copy of default settings
JSPLUMB = JSPLUMB_DEFAULTS.copy()

# Override with user settings from settings.py
JSPLUMB.update(getattr(settings, 'JSPLUMB', {}))


def get_jsplumb_setting(setting, default=None):
    """
    Read a setting
    """
    return JSPLUMB.get(setting, default)


#def jsplumb_defaults_url():
def jsplumb_settings_script():  # defaults

    #have to generate stuff like render mode
    # jsPlumb.draggable($(".window"));
    #jsPlumb.setRenderMode(jsPlumb.SVG);
    # animate TorF,
    #jsPlumb.animate("1", {"left": 225,"top": 120},{duration: 1000});

    js_script = '''
    <script>
        alert('welcome to jsPlumb, settings loaded!')
        jsPlumb.draggable($(".window"));
        $(document).ready(function() {
            $(window).resize(function() {
                jsPlumb.repaintEverything();
            });
            jsPlumb.setRenderMode('jsPlumb.SVG');
            });
    </script>'''

    return js_script


def jsplumb_url():
    """
    Prefix a relative url with the jsplumb url
    """
    return get_jsplumb_setting('jsplumb_url')


# Same as above ...
'''
def javascript_url():
    """
    Prefix a relative url with the jsplumb url
    """
    return get_jsplumb_setting('jsplumb_url')
'''

def jquery_url():
    """
    Return the full url to jQuery file to use
    """
    return get_jsplumb_setting('jquery_url')


def css_url():
    """
    Return the full url to the default CSS file
    """
    return get_jsplumb_setting('css_url') #or jsplumb_url('css/bootstrap.min.css')

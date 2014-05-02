# -*- coding: utf-8 -*-
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator  # no work, only in form?
from django.db.models.signals import post_delete
from django.dispatch import receiver

from locations.models import Location

# Everythign has to be drawn in template when doc is ready
# endpoint and anchor are 1:1 entities

# LOAD
''' BULK LOADING, suspend drawing (faster speeds)
jsPlumb.setSuspendDrawing(true);
...
- load up all your data here -
...
jsPlumb.setSuspendDrawing(false, true);

'''
# can be though of as the container
# have to define a drawing to add elements to, then can load drawing in either save or view mode

''' DEFAULT SETTINGS, only worried about these when editing , not when loading for viewing, worry bout this later
Anchor : "BottomCenter",
Anchors : [ null, null ],
ConnectionsDetachable   : true,
ConnectionOverlays  : [],
Connector : "Bezier",
Container : null,
DoNotThrowErrors  : false,
DragOptions : { },
DropOptions : { },
Endpoint : "Dot",
Endpoints : [ null, null ],
EndpointOverlays : [ ],
EndpointStyle : { fillStyle : "#456" },
EndpointStyles : [ null, null ],
EndpointHoverStyle : null,
EndpointHoverStyles : [ null, null ],
HoverPaintStyle : null,
LabelStyle : { color : "black" },
LogEnabled : false,
Overlays : [ ],
MaxConnections : 1,
PaintStyle : { lineWidth : 8, strokeStyle : "#456" },
ReattachConnections : false,
RenderMode : "svg",
Scope : "jsPlumb_DefaultScope"
'''

# anchor is 1-1 w/ element
# element has 0 to many endpoints (that appear where anchor is set)
# endpoint to endpoint has a connection
# a connection has 0 to many overlays

#LocationDrawing to extend PlumbDrawing!! with added location FK


class PlumbDrawing(models.Model):  # default Scope, set as 1, no mult. instances atm.
    #animate elements option ?
    name = models.CharField(max_length=75, blank=True, null=True)
    container_name = models.CharField(max_length=75, blank=True, null=True)  # jsPlumb.Defaults.Container = $("body"); or "containerId";

    #elements = models.ManyToManyField("PlumbElement", through='PlumbDrawingElement')

    #jsPlumb.Defaults.Container = $("body");
    # jsPlumb.Defaults.Container = "containerId";

    #make defaults set by javascript, instance will be 1 for the time being
    #defaults (connector, anchors, paintstyle, endpoint/style, )
    '''
    firstInstance.importDefaults({
      Connector : [ "Bezier", { curviness: 150 } ],
      Anchors : [ "TopCenter", "BottomCenter" ]
    });
      PaintStyle:{
    lineWidth:6,
    strokeStyle:"#567567",
    outlineColor:"black",
    outlineWidth:1
    },
    Connector:[ "Bezier", { curviness: 30 } ],
    Endpoint:[ "Dot", { radius:5 } ],
    EndpointStyle : { fillStyle: "#567567"  },
    Anchor : [ 0.5, 0.5, 1, 1 ]

    '''
    # will comprise of elements





# PaintStyle ? ?

#Circle used as Ellipse, Square used as Rectangle
SHAPE_CHOICE = (
    ('Ellipse', 'Ellipse or Circle'),
    ('Triangle', 'Triangle'),
    #('Diamond', 'Diamond'),  # Isn't same as square but rotated?
    ('Rectangle', 'Rectangle or Square'),
)

#from django.core.files.storage import FileSystemStorage
#from mandala.settings import PRIVATE_DIR
#fs = FileSystemStorage(location=PRIVATE_DIR, base_url='/')

#fs_relative_file_path = 'locations/photos/'
#
#def generate_path(instance, filename):
#
#    ext = filename.split('.')[-1]
#    filename = "{0}.{1}".format(uuid.uuid4(), ext)
#    return os.path.join(instance.fs_relative_file_path, filename)


class PlumbAnchor(models.Model):
    """ This is a perimeter anchor, it is the only type needed/ supported
    """

    #name ?
    shape = models.CharField(blank=False, null=False, choices=SHAPE_CHOICE, default='Rectangle', max_length=15)
    rotation = models.SmallIntegerField(validators=[MinValueValidator(-360), MaxValueValidator(360)], default=0)
    image = models.ImageField(upload_to='jsplumb_images', blank=True, null=True)

    def save(self, *args, **kwargs):
        """ Override save """
        #self.full_clean(exclude=None)
        if self.rotation > 360:  # Ensure that rotation is between -360 and 360
            self.rotation = 360
        elif self.rotation < -360:
            self.rotation = -360

        super(PlumbAnchor, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{0}:{1}°'.format(self.shape, self.rotation)


# cleans up the deleted photo model files afterwards
@receiver(post_delete, sender=PlumbAnchor)
def plumb_image_post_delete_handler(sender, **kwargs):
    element_item = kwargs['instance']
    try:
        storage, path = element_item.image.storage, element_item.image.path
        storage.delete(path)
    except Exception:
        pass


# Abstract class, but not really.. can be used alone
class PlumbElement(models.Model):

    #in html class can use <plumb_element_id_#>
    element_name = models.CharField(max_length=75, blank=True, null=True)  # contains name @ this level?, optional yes
    anchor = models.ForeignKey(PlumbAnchor)

    #class Meta:  # can't make relation, AssertionError: ForeignKey cannot define a relation with abstract class PlumbElement
    #    abstract = True


    #height = models.PositiveSmallIntegerField()
    #width = models.PositiveSmallIntegerField()

    # used for perimeter anchor
    ##shape = models.CharField(blank=False, null=False, choices=SHAPE_CHOICE, default='Rectangle', max_length=15)
    ##rotation = models.SmallIntegerField(validators=[MinValueValidator(-360), MaxValueValidator(360)], default=0)
    ##image = models.ImageField(upload_to='jsplumb_elements', blank=True, null=True)  # optional image
    #draw the shape if no image inputted & shape is circle or triangel or any shape w/ rotation
    # apply the rotation after drawing the shape!

    # if triangle or elipse selected w/o photo then generate a photo. Transparent w/ gray fill. black border?

    # draggable
    # leave draggable stuff to drawing for now
    # draggable = boolean, jsPlumb.draggable($(".someClass")); or can use element id (perferred)
    # drag_containment = default is the container_name it belongs to.
    #
    #jsPlumb.draggable($("someSelector"), {
    #  containment:"parent"
    #});

    '''
    def save(self, *args, **kwargs):
        """ Override save """
        #self.full_clean(exclude=None)
        if self.rotation > 360:  # Ensure that rotation is between -360 and 360
            self.rotation = 360
        elif self.rotation < -360:
            self.rotation = -360

        super(PlumbElement, self).save(*args, **kwargs)
    '''

    def __unicode__(self):
        return u'{0}:{1}'.format(self.element_name, self.anchor)


# Stores the Many-Many relationship, as Elements can be used in many Drawings, Drawings contain many Elements
class PlumbDrawnElement(models.Model):
    #name = models.CharField(max_length=75, blank=True, null=True)

    drawing = models.ForeignKey(PlumbDrawing)
    element = models.ForeignKey(PlumbElement)
    left = models.PositiveSmallIntegerField(blank=True, null=True)  # x val in current drawing, relative to container
    top = models.PositiveSmallIntegerField(blank=True, null=True)  # y val in current drawing, relative to container

    class Meta:
        unique_together = ("drawing", "element")  # cant use 2 elements on 1 drawing!

    def __unicode__(self):
        return u'{0}:{1}'.format(self.drawing, self.element)

#An element will have multiple end-points
# jsPlumb.addEndpoint(someDiv, { endpoint options });

ENDPOINT_TYPE_CHOICES = (
    ('Dot', 'Dot'),  # Constructor Params: radius, cssClass, hoverClass
    ('Rectangle', 'Rectangle'),  # Constructor Params: width, height, cssClass, hoverClass
    #('Blank', 'Blank'),  # does not support dragging connections!
    #('Image', 'Image'),  # Constructor Params: src, cssClass, hoverClass
)


#For simplicity, defaults used for endpoint type constructors
class PlumbEndpoint(models.Model):  # var e0 = jsPlumb.addEndpoint("node0"),
    # set and use id generated here by django (or jsplubm sets own! )
    #name = models.CharField(max_length=75, blank=True, null=True)
    drawn_element = models.ForeignKey(PlumbDrawnElement)
    max_connections = models.PositiveSmallIntegerField(default=1)  # default is 1 conn
    is_source = models.BooleanField(default=True)
    is_target = models.BooleanField(default=True)
    type = models.CharField(max_length=20, default='Dot', null=False, blank=False, choices=ENDPOINT_TYPE_CHOICES)
    #width
    #height (of the endpoint) # have 1 cssClass and have all stuff in there
    #cssClass "myEndpoint"
    #anchor 1-1 connection to foreign key

    # CSS
    # type -> Rectangle, Dot, etc..  <- styling, CSS
    # options (JSON):  { endpoint options }
    # EndPointStyle ? JSON options

    #ex js
    #jsPlumb.addEndpoint(["1", "2"]);
    #//jsPlumb.addEndpoint("1", {isSource: true, isTarget: true});
    #jsPlumb.addEndpoint(["1", "2"], {isSource: true, isTarget: true, endpoint: "Rectangle", maxConnections: 2});
    #jsPlumb.addEndpoint(["1", "2"], {isSource: true, isTarget: true, endpoint: "Dot", anchor: "AutoDefault", maxConnections: 2});
    def __unicode__(self):
        return u'{0}:{1}'.format(self.id, self.drawing_element)


# a connector will be between two endpoints
# for conn to work, src tgt elements need to be siblings (same parent), not in diff divs...
class PlumbConnector(models.Model):  # jsPlumb.connect({ source:e0, target:e1 });

    #name = models.CharField(max_length=75, blank=True, null=True)
    #cssClass
    # type
    # options (JSON):  ( curviness: , etc.. ) { curviness:100 }
    #

    #OnetoOne field? NO a target source endpoint can be re-used technically, limit by max_conn, is src is target attrs
    source_endpoint = models.ForeignKey(PlumbEndpoint, related_name="plumbconnector_source_set")
    target_endpoint = models.ForeignKey(PlumbEndpoint, related_name="plumbconnector_target_set")
    # ( use end points), jsPlumb.connect({ source:e0, target:e1 });

    def __unicode__(self):
        return u'PlumbConnector for endpoints {0}:{1}'.format(self.source_endpoint.id, self.target_endpoint.id)


#A connection can have multiple overlays
class PlumbOverlay(models.Model):

    name = models.CharField(max_length=75, blank=True, null=True)
    connector = models.ForeignKey(PlumbConnector, blank=True, null=True)  # 0 to many
    #cssClass <- can be passed as option
    #options (jSON) , { foldback:0.2 }, { cssClass:"labelClass" }
    #label, arrow, image ?
    #examples:
    #[ "Arrow", { foldback:0.2 }, common ],
    #[ "Label", { cssClass:"labelClass" } ]


# NO NEED for it!
# for simplicity, only perimeter anchors will be used, won't need this here.
#class PlumbAnchor(models.Model):  # and anchor  (1-1 w/ element , not endpoint!), defines loc of endpoint

    #name = models.CharField(max_length=75, blank=True, null=True)
    # anchor (Top, Bottom (static/dynamic), auto, perimeter, continuous etc.. )
    # type: Static: Top (also aliased as TopCenter) - TopRight - Right (also aliased as RightMiddle) - BottomRight - Bottom (also aliased as BottomCenter) - BottomLeft - Left (also aliased as LeftMiddle) - TopLeft
    #  Dynamic, Perimeter, Continuous

    #if type = Perimeter, shape must be described in element!

'''
Creating table jsplumber_plumbdrawing
Creating table jsplumber_locationdrawing
Creating table jsplumber_plumbanchor
Creating table jsplumber_plumbelement
Creating table jsplumber_locationasset
Creating table jsplumber_plumbdrawnelement
Creating table jsplumber_plumbendpoint
Creating table jsplumber_plumbconnector
Creating table jsplumber_plumboverlay
'''
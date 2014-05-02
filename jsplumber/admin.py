from django.contrib import admin

# Register your models here.
from models import PlumbElement
from models import PlumbDrawnElement
from models import PlumbDrawing
from models import PlumbAnchor

from models import PlumbEndpoint
from models import PlumbConnector

#admin.site.register(PlumbElement)
#admin.site.register(PlumbDrawing)
#admin.site.register(PlumbDrawnElement)
#admin.site.register(PlumbDrawingElement)

#class LocationAssetInline(admin.TabularInline):
#    model = LocationAsset
#    extra = 1


class PlumbDrawnElementInline(admin.TabularInline):
    model = PlumbDrawnElement
    extra = 1

    #fk_name = "element"
#class PlumbDrawnElementInlines(admin.TabularInline):  # StackedInline vs TabularInline
#    model = PlumbDrawnElement





class PlumbDrawingAdmin(admin.ModelAdmin):
    inlines = [
        PlumbDrawnElementInline,
    ]

admin.site.register(PlumbDrawing, PlumbDrawingAdmin)


class PlumbElementAdmin(admin.ModelAdmin):
    inlines = [
        PlumbDrawnElementInline,
    ]

admin.site.register(PlumbElement, PlumbElementAdmin)


#### APP SPECIFIC

#class LocationAssetInline(admin.TabularInline):
#    model = PlumbDrawnElement
#    extra = 1
#    #fk_name = "element"

'''
class LocationDrawingAdmin(admin.ModelAdmin):
    inlines = [
        PlumbDrawnElementInline,
    ]


class LocationAssetAdmin(admin.ModelAdmin):
    inlines = [
        PlumbDrawnElementInline,
    ]


admin.site.register(LocationDrawingAdmin)
admin.site.register(LocationAssetAdmin)

admin.site.register(LocationAsset)
admin.site.register(LocationDrawing)
admin.site.register(PlumbDrawnElement)
'''

### END APP SPECIFIC





#admin.site.register(PlumbElement)
''' WHY NO WORK?
class PlumbElementInline(admin.TabularInline):
    model = PlumbElement


class PlumbDrawingAdmin(admin.ModelAdmin):
    #exclude = ['active']

    inlines = [
        PlumbElementInline,
    ]
admin.site.register(PlumbDrawingAdmin)
'''


#admin.site.register(PlumbEndpoint)
#admin.site.register(PlumbConnector)
admin.site.register(PlumbAnchor)
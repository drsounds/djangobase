from django.contrib import admin

from adminsortable.admin import (SortableAdmin,  SortableStackedInline, NonSortableParentAdmin)

from djangobase.models import Collection, Feature, CollectionGroup, Website, Column, ColumnGroup


class CollectionGroupCollectionTabularInline(SortableStackedInline):
    model = CollectionGroup.collections.through
    list_display = ['name', 'slug']
    extra = 1


class CollectionGroupAdmin(SortableAdmin):
    inlines = [
        CollectionGroupCollectionTabularInline
    ]


class CollectionColumnGroupTabularInline(SortableStackedInline):
    model = ColumnGroup.collections.through
    list_display = ['name', 'slug']
    extra = 1


class CollectionAdmin(SortableAdmin):
    inlines = [
        CollectionColumnGroupTabularInline
    ]


class ColumnTabularInline(SortableStackedInline):
    model = Column.column_groups.through
    list_display = ['name', 'slug']
    extra = 1



class FeatureTabularInline(SortableStackedInline):
    model = Feature.websites.through
    list_display = ['name', 'slug']
    extra = 1

class FeatureCollectionTabularInline(SortableStackedInline):
    model = Collection.features.through
    list_display = ['name', 'slug']
    extra = 1


class FeatureAdmin(SortableAdmin):
    inlines = [
        FeatureCollectionTabularInline
    ]


class ColumnGroupAdmin(SortableAdmin):
    inlines = [
        ColumnTabularInline
    ]


class WebsiteAdmin(SortableAdmin):
    inlines = [
        FeatureTabularInline
    ]


class ColumnAdmin(admin.ModelAdmin):
    pass


admin.site.register(CollectionGroup, CollectionGroupAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(ColumnGroup, ColumnGroupAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Feature, FeatureAdmin)

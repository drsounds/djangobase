from django.contrib import admin

from adminsortable.admin import (SortableAdmin,  SortableStackedInline, NonSortableParentAdmin)

from djangobase.models import Collection, Website, Column, ColumnGroup


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


class ColumnGroupAdmin(SortableAdmin):
    inlines = [
        ColumnTabularInline
    ]


class SiteAdmin(admin.ModelAdmin):
    pass


class ColumnAdmin(admin.ModelAdmin):
    pass


admin.site.register(Collection, CollectionAdmin)
admin.site.register(Website, SiteAdmin)
admin.site.register(ColumnGroup, ColumnGroupAdmin)
admin.site.register(Column, ColumnAdmin)

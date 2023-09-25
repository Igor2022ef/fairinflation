from django.contrib import admin
from watchinflation.models import *


from import_export import resources
from import_export.admin import ImportExportModelAdmin

class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

# класс обработки данных
class BuildgraphResource(resources.ModelResource):
    class Meta:
        model = Buildgraph
        # import_id_fields = ('name',)
        # skip_unchanged = True
        # report_skipped = True

# вывод данных на странице
class BuildgraphAdmin(ImportExportModelAdmin):
    resource_classes = [BuildgraphResource]
    list_display = ('name_product',)
    search_fields = ('name_product',)

admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Buildgraph, BuildgraphAdmin)



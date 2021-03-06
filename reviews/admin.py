from django.contrib import admin

from .models import Wine, Review, Cluster, Fake

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('wine', 'user_id','rating', 'user_name', 'comment', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']
    

class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name', 'get_members']


admin.site.register(Wine)
admin.site.register(Fake)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Cluster, ClusterAdmin)
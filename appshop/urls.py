from django.urls import path
from appshop.views import index, index_item, add_item, update_item, delete_item, sortname, ItemListView

app_name="appshop"

urlpatterns = [
    path("", index, name="index"),
    path("main/", index),
    path("product/<id>/", index_item, name="detail"),
    path("additem/", add_item, name="additem"),
    path("updateitem/<id>/", update_item, name="update_item"),
    path("deleteitem/<id>/", delete_item, name="delete_item"),
    path("name_sorted/", sortname, name="indexname"),
    path("items/", ItemListView.as_view(), name='item-list'),
]
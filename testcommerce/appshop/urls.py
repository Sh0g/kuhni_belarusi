from django.urls import path
from appshop.views import index, index_item

app_name="appshop"

urlpatterns = [
    path("main/", index),
    path("product/<id>/", index_item, name="detail"),
]
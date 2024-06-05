import graphene
from graphene_django import DjangoObjectType
from models import Item

class ItemType(DjangoObjectType):
    class Meta:
        model = Item

class Query(graphene.ObjectType):
    items = graphene.List(ItemType)

    def resolve_items(self, info):
        return Item.objects.all()

schema = graphene.Schema(query=Query)
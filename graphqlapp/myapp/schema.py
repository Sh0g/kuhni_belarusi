import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from myapp.models import Name, Item
class NameType(DjangoObjectType):
    class Meta:
        model = Name
class PriceType(DjangoObjectType):
    class Meta:
        model = Item

class Query(ObjectType):
    name = graphene.Field(NameType, id=graphene.Int())
    price = graphene.Field(PriceType, id=graphene.Int())
    names = graphene.List(NameType)
    prices = graphene.List(PriceType)
    def resolve_name(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Name.objects.get(pk=id)
        return None
    def resolve_price(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Item.objects.get(pk=id)
        return None
    def resolve_names(self, info, **kwargs):
        return Name.objects.all()
    def resolve_prices(self, info, **kwargs):
        return Item.objects.all()

class NameInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
class PriceInput(graphene.InputObjectType):
    id = graphene.ID()
    names = graphene.List(NameInput)
    price = graphene.Int()

class CreateName(graphene.Mutation):
    class Arguments:
        input = NameInput(required=True)
    ok = graphene.Boolean()
    name = graphene.Field(NameType)
    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        name_instance = Name(name=input.name)
        name_instance.save()
        return CreateName(ok=ok, actor=name_instance)
class UpdateName(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = NameInput(required=True)
    ok = graphene.Boolean()
    name = graphene.Field(NameType)
    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        name_instance = Name.objects.get(pk=id)
        if name_instance:
            ok = True
            name_instance.name = input.name
            name_instance.save()
            return UpdateName(ok=ok, name=name_instance)
        return UpdateName(ok=ok, actor=None)

class CreatePrice(graphene.Mutation):
    class Arguments:
        input = PriceInput(required=True)
    ok = graphene.Boolean()
    price = graphene.Field(PriceType)
    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        names = []
        for name_input in input.names:
            name = Name.objects.get(pk=name_input.id)
            if name is None:
                return CreatePrice(ok=False, price=None)
            names.append(name)
        price_instance = Item(
            price=input.price
        )
        price_instance.save()
        price_instance.actors.set(names)
        return CreateName(ok=ok, price=price_instance)
class UpdatePrice(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = PriceInput(required=True)
    ok = graphene.Boolean()
    price = graphene.Field(PriceType)
    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        price_instance = Item.objects.get(pk=id)
        if price_instance:
            ok = True
            names = []
            for name_input in input.names:
                name = Name.objects.get(pk=name_input.id)
                if name is None:
                    return CreatePrice(ok=False, price=None)
                names.append(name)
            price_instance = Item(
                price=input.price,
            )
            price_instance.save()
            price_instance.names.set(names)
            return UpdatePrice(ok=ok, price=price_instance)
        return UpdatePrice(ok=ok, price=None)

class Mutation(graphene.ObjectType):
    create_name = CreateName.Field()
    update_name = UpdateName.Field()
    create_price = CreatePrice.Field()
    update_price = UpdatePrice.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
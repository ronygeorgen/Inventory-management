import factory
import faker
from django.contrib.auth.models import User
from inventory_app.models import Item

# Generate realistic fake data
fake = faker.Faker()

# User factory
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.lazy_attribute(lambda _: fake.user_name())
    email = factory.lazy_attribute(lambda _: fake.email())
    password = factory.PostGenerationMethodCall("set_password", "password123")  

# Item factory
class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item
    name = factory.LazyAttribute(lambda _: fake.word().capitalize())
    description = factory.LazyAttribute(lambda _: fake.sentence())
    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=100))
    price = factory.LazyAttribute(lambda _: fake.pydecimal(left_digits=3, right_digits=2, positive=True))
    created_by = factory.SubFactory(UserFactory)
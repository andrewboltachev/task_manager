import factory
from django.contrib.auth import get_user_model

from tasks.models import Task

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.Sequence(lambda n: f'user_{n}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    
    # Set a known password so we can log in during tests
    password = factory.PostGenerationMethodCall('set_password', 'password123')

class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text')
    status = 'new'
    # SubFactory means "Create a User automatically if one isn't provided"
    creator = factory.SubFactory(UserFactory)

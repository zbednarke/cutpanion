import factory
from django.db.models import signals
from django.contrib.auth import get_user_model


User = get_user_model()

@factory.django.mute_signals(signals.post_save)
class UserFactory(factory.django.DjangoModelFactory):

    username = factory.Sequence(lambda n: f"simple_user{n}")
    myuser = factory.SubFactory("accounts.tests.factories.MyUserFactory")
    is_superuser = False
    is_active = True

    class Meta:
        model = User

    @classmethod
    def build(cls, kwargs):
        """
        If the password if supplied, hash and salt it.
        """
        user = super().build(kwargs)
        if user.password:
            user.set_password(user.password)
        return user

    @classmethod
    def create(cls, kwargs):
        return cls.create_batch(1, kwargs)[0]

    # @classmethod
    # def create_batch(cls, size, **kwargs):
    #     """
    #     Similar to create_batch but more efficient.

    #     To avoid O(n) queries, we create 2 queries irregardless of the size:
    #     * one for the User insert
    #     * the other for the MyUser insert
    #     """
    #     users, _ = create_user_myuser_batch(cls, size, kwargs)
    #     return users
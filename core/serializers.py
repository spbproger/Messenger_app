from rest_framework import serializers
from django.utils import timezone
from django.core.validators import RegexValidator
from .models import Author, Publication, Comment


class EmailValidator:
    def __call__(self, value):
        valid_domains = ("yandex.ru", "mail.ru")
        current_domain = value.split("@")[-1]
        if current_domain not in valid_domains:
            raise serializers.ValidationError("Ваш домен отличается от разрешенных: mail.ru, yandex.ru")


class AuthorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[
        RegexValidator(r'[A-Za-z0-9@#$%^&+=]{8,}', message="Пароль должен состоять не менее, "
                                                           "чем из 8 букв, знаков и содержать цифры")])
    email = serializers.EmailField(validators=[EmailValidator()])

    class Meta:
        model = Author
        fields = '__all__'

    def create(self, validated_data):
        author = super().create(validated_data)
        author.set_password(author.password)
        author.save()
        return author


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=Author.objects.all(), slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'


class HeadingValidator:
    def __call__(self, value):
        bad_words = ['ерунда', 'глупость', 'чепуха']
        for word in bad_words:
            if word in value.lower():
                raise serializers.ValidationError(r'Использовать слова "ерунда", "глупость", "чепуха" запрещено!')


class PublicationSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=Author.objects.all(), slug_field='username')
    comment = serializers.SlugRelatedField(queryset=Comment.objects.all(), slug_field='cdescription', many=True)
    heading = serializers.CharField(validators=[HeadingValidator()])

    class Meta:
        model = Publication
        fields = '__all__'

    def validate_author(self, value):
        if not value.is_staff:
            if value.birthday is None:
                raise serializers.ValidationError("Укажите дату Вашего рождения.")
            age = (timezone.now().date() - value.birthday).days // 365
            if age < 18:
                raise serializers.ValidationError("Публикации разрешены лицам старше 18 лет.")
            return value
        return value




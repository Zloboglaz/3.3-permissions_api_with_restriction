from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    # creator = UserSerializer(
    #     read_only=True,
    # )

    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ['creator']

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию

        if self.instance is None:
            request = self.context.get('request')
            # Убедимся, что пользователь аутентифицирован
            if request and request.user.is_authenticated:
                # Считаем количество открытых объявлений у этого пользователя
                open_count = Advertisement.objects.filter(
                    creator=request.user,
                    status='OPEN'
                ).count()
                # Если уже 10 или больше при попытке создать 11 запрещено
                if open_count >= 10:
                    raise serializers.ValidationError(
                        "У вас не может быть больше 10 открытых объявлений."
                    )
        return data

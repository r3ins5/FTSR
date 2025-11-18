from .models import Coord, Level, Pereval, Images, MyUser
from rest_framework import serializers


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coord
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImagesSerializer(serializers.ModelSerializer):
    data = serializers.URLField()

    class Meta:
        model = Images
        fields = ['data', 'title']


class UserSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        self.is_valid()
        user = MyUser.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            new_user = MyUser.objects.create(
                fam=self.validated_data.get('fam'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
                phone=self.validated_data.get('phone'),
                email=self.validated_data.get('email'),
            )
            return new_user

    class Meta:
        model = MyUser
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class PerevalSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    status = serializers.CharField(read_only=True)
    user = UserSerializer()
    coords = CoordSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = Pereval
        fields = ['id', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time',
                  'user', 'coords', 'level', 'images', 'status']

    def create(self, validated_data):
        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        images = validated_data.pop('images')
        levels = validated_data.pop('level')

        current_user = MyUser.objects.filter(email=user['email'])
        if current_user.exists():
            user_serializers = UserSerializer(data=user)
            user_serializers.is_valid(raise_exception=True)
            user = user_serializers.save()
        else:
            user = MyUser.objects.create(**user)

        coords = Coord.objects.create(**coords)
        levels = Level.objects.create(**levels)
        pereval_new = Pereval.objects.create(**validated_data, user=user, coords=coords, level=levels)

        if images:
            for img in images:
                title = img.pop('title')
                data = img.pop('data')
                Images.objects.create(pereval=pereval_new, title=title, data=data)

        return pereval_new

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            validating_user_fields = [
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(validating_user_fields):
                raise serializers.ValidationError({'Данные пользователя не могут быть изменены'})
        return data

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        coords_data = validated_data.pop('coords', None)
        level_data = validated_data.pop('level', None)
        images_data = validated_data.pop('images', None)

        instance.beauty_title = validated_data.get('beauty_title', instance.beauty_title)
        instance.title = validated_data.get('title', instance.title)
        instance.other_titles = validated_data.get('other_titles', instance.other_titles)
        instance.connect = validated_data.get('connect', instance.connect)

        UserSerializer().update(instance.user, user_data)
        CoordSerializer().update(instance.coords, coords_data)
        LevelSerializer().update(instance.level, level_data)

        for image_data in images_data:
            image_id = image_data.get('id', None)
            if image_id:
                image_instance = Images.objects.get(id=image_id)
                ImagesSerializer().update(image_instance, image_data)
            else:
                Images.objects.create(pereval=instance, **image_data)

        instance.save()
        return instance
from django.db import models
from .services import get_path_upload_photo
from django.core.validators import RegexValidator
# Create your models here.
check_number = RegexValidator(regex=r'^\+\d{11}$',
                              message="Номер телефона должен быть введён в следующем формате: '+78005553535' 11 цифр.")
class MyUser(models.Model):
    name = models.CharField(max_length=150)
    fam = models.CharField(max_length=150)
    otc = models.CharField(max_length=150)
    phone = models.CharField(validators=[check_number], max_length=15, blank=True)
    email = models.CharField(max_length=150)
    objects = models.Manager()

    USERNAME_FIELD = 'name'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'fam', 'otc', 'phone']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name}_{self.fam}_{self.otc}_{self.phone}_{self.email}'


class Coord(models.Model):
    latitude = models.DecimalField(decimal_places=8, max_digits=10)
    longitude = models.DecimalField(decimal_places=8, max_digits=10)
    height = models.IntegerField(default=0)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Координаты'
        verbose_name_plural = 'Координаты'


class Level(models.Model):
    CHOICE_LEVEL = (
        (' ', ' '),
        ('1A', '1A'),
        ('2A', '2A'),
        ('3A', '3A'),
        ('4A', '4A'),
    )

    winter = models.CharField(max_length=2, choices=CHOICE_LEVEL, default=' ')
    spring = models.CharField(max_length=2, choices=CHOICE_LEVEL, default=' ')
    summer = models.CharField(max_length=2, choices=CHOICE_LEVEL, default=' ')
    autumn = models.CharField(max_length=2, choices=CHOICE_LEVEL, default=' ')
    objects = models.Manager()

    class Meta:
        verbose_name = 'Уровень'
        verbose_name_plural = 'Уровни'


class Pereval(models.Model):
    CHOICE_STATUS = (
        ('new', 'новый'),
        ('pending', 'модератор взял в работу'),
        ('approved', 'модерация прошла успешно'),
        ('rejected', 'модерация прошла, информация не принята'),
    )
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_title = models.CharField(max_length=255)
    content = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=CHOICE_STATUS, default='new')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user')
    coord = models.ForeignKey(Coord, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Перевал'
        verbose_name_plural = 'Перевалы'

    def __str__(self):
        return f'{self.beauty_title}_{self.title}_{self.id}'

class Images(models.Model):
    title = models.CharField(max_length=255)
    data = models.ImageField(upload_to=get_path_upload_photo, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE,related_name='images')
    objects = models.Manager()

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображение'

    def __str__(self):
        return f'{self.title}'

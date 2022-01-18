from django.db import models

from blog.const import FORMAT


# class AdvUser(AbstractUser):
#     is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
#     send_messages = models.BooleanField(default=True, verbose_name='Слать оповещения о новых комментариях?')


class User(models.Model):
    phone_number = models.CharField('Номер телефона', max_length=12, null=True, blank=True)
    username = models.CharField('Имя клиента', max_length=255)
    mail_adr = models.EmailField('Эл.почта', max_length=254)
    # is_active = models.BooleanField('Прошёл активацию?', default=True, blank=True)

    class Meta:
        verbose_name = 'Неавторизованный пользователь'
        verbose_name_plural = 'Неавторизованные пользователи'


class Training(models.Model):
    title = models.CharField('Заголовок', max_length=50)
    content = models.TextField('Описание', blank=True, null=True)
    price = models.FloatField('Стоимость', blank=True, null=True)
    format = models.CharField('Формат тренировок', max_length=20,  choices=FORMAT, blank=True, null=True)
    date_created = models.DateField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тренировку'
        verbose_name_plural = 'Тренировки'
        ordering = ['-id']

#
# class Format(models.Model):
#     title = models.CharField('Формат занятий', max_length=50)
#     content = models.TextField('Описание', blank=True, null=True)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name = 'Формат занятий'
#         verbose_name_plural = 'Форматы занятий'
#         ordering = ['title']

import datetime
from django.db import models
from django.db.models import PROTECT
from django.utils import timezone


class Category(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Тип заметки"
        verbose_name_plural = "Тип заметки"


class Note(models.Model):
    note = models.TextField(blank=True, verbose_name='Заметка')
    data = models.PositiveSmallIntegerField(default=str(timezone.now().year) +
                                                    str(timezone.now().month) +
                                                    str(timezone.now().day), verbose_name='Дата')

    category = models.ForeignKey(Category, on_delete=PROTECT, verbose_name="Тип заметки")

    def __str__(self):
        return self.note[:30]

    class Meta:
        ordering = ('-data',)
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

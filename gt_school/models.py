from django.db import models


class EventTypeChoices(models.TextChoices):
    BLUE = '', '一般事务'
    GREEN = 'success', '常规事务'
    YELLOW = 'warning', '重要事务'
    RED = 'error', '特殊事务'


class CalendarEvent(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField(null=True, blank=True, max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    all_day = models.BooleanField(default=False)
    url = models.CharField(null=True, blank=True)
    type = models.CharField(max_length=20,
                            choices=EventTypeChoices,
                            default=EventTypeChoices.BLUE)

    class Meta:
        db_table = "calendar_event"
        verbose_name = verbose_name_plural = '校历事件'

    def __str__(self):
        return self.title

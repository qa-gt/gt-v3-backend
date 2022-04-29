from django.db import models


class TimeTypeChoices(models.IntegerChoices):
    WHOLE_DAY = 0, '全天'
    START = 1, '开始时间'
    START_AND_END = 2, '开始时间和结束时间'


class EventTypeChoices(models.TextChoices):
    BLUE = '', '一般事务'
    GREEN = 'success', '常规事务'
    YELLOW = 'warning', '重要事务'
    RED = 'danger', '特殊事务'


class CalendarEvent(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField(null=True, blank=True, max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    timeType = models.SmallIntegerField(choices=TimeTypeChoices.choices,
                                        default=TimeTypeChoices.WHOLE_DAY)
    url = models.CharField(null=True, blank=True, max_length=500)
    type = models.CharField(max_length=20,
                            choices=EventTypeChoices.choices,
                            default=EventTypeChoices.BLUE)

    class Meta:
        db_table = "calendar_event"
        verbose_name = verbose_name_plural = '校历事件'

    def __str__(self):
        return self.title

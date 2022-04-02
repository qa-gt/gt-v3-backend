from .models import *


def add_notice(recipient, title, content, url=None):
    if not content:
        content = title
    if len(title) > 30:
        title = title[:30] + '...'
    if len(content) > 70:
        content = content[:70] + '...'
    Notice.objects.get_or_create(recipient=recipient,
                                 title=title,
                                 content=content,
                                 url=url,
                                 state=NoticeStateChoices.UNREAD)

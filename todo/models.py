from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Todo(models.Model):
    author = models.ForeignKey(User , related_name = "author_set", on_delete = models.CASCADE)  # 작성자
    timeline =  models.DateTimeField(auto_now_add = True)   # 작성 시간
    date = models.DateField(null = False, blank = False)    # 투두 언제까지 해야 하는지
    contents = models.CharField(max_length = 300, null = False, blank = False)  # 투두 컨텐츠

    STATE_COMPLETE = "complete"
    STATE_ONGOING = "ongoing"
    STATE_CHOICES = (
        (STATE_COMPLETE, "complete"), 
        (STATE_ONGOING, "ongoing"), 
    )
    state = models.CharField(max_length = 50, choices = STATE_CHOICES , default = "ongoing")  # 투두의 상태
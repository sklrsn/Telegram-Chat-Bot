from django.db import models
from datetime import datetime

"""
@Class_Name: ApplicationUser
@Params: user_id, first_name,username
"""


class ApplicationUser(models.Model):
    user_id = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    username = models.CharField(max_length=50)

    class Meta:
        db_table = "ApplicationUser"
        verbose_name = "ApplicationUser"
        verbose_name_plural = "ApplicationUsers"

    def __str__(self):
        return self.user_id


"""
@Class_Name: MessageHolder
@Params: user_id, message_id,message,message_date
"""


class MessageHolder(models.Model):
    user_id = models.ForeignKey(ApplicationUser, to_field="user_id", db_column="user_id")
    message_id = models.BigIntegerField(blank=True)
    message = models.TextField(max_length=1000)
    message_date = models.DateTimeField(default=datetime.today())

    class Meta:
        db_table = "MessageHolder"
        verbose_name = "MessageHolder"
        verbose_name_plural = "MessageHolders"

    def __str__(self):
        return str(self.message_id)

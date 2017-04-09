from django.db import models


class ApplicationUser(models.Model):
    user_id = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    username = models.CharField(max_length=50)

    class Meta:
        db_table = "ApplicationUser"

    def __str__(self):
        return self.user_id


class MessageHolder(models.Model):
    user_id = models.ForeignKey(ApplicationUser, to_field="user_id", db_column="user_id")
    message_id = models.BigIntegerField(blank=True)
    message = models.TextField(max_length=1000)

    # Add date field
    class Meta:
        db_table = "MessageHolder"

    def __str__(self):
        return str(self.message_id)

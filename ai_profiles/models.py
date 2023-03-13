from django.db import models


# Create your models here.
class BotProfile(models.Model):
    bot_id = models.CharField(max_length=200)
    gender = models.CharField(max_length=1)
    age = models.IntegerField()
    profession = models.TextField(null=True)
    hobbies = models.JSONField()
    favorites = models.JSONField()
    profile_image = models.ImageField(upload_to='images/')

    def get_id(self):
        return self.bot_id

    def __str__(self):
        return f"ID: {self.bot_id}, Gender: {self.gender}, Age: {self.age}, Hobbies: {self.hobbies}, Profession: {self.profession}, Favorites: {self.favorites}"

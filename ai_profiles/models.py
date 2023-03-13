from django.db import models


# Create your models here.-
class BotProfile(models.Model):
    bot_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    age = models.IntegerField()
    bio = models.CharField(max_length=300)
    profession = models.TextField(null=True)
    hobbies = models.JSONField()
    favorites = models.JSONField()
    profile_image = models.ImageField(upload_to='images/')

    def get_id(self):
        return self.bot_id

    def __str__(self):
        return f"ID: {self.bot_id}, Name: {self.name}, Gender: {self.gender}, Age: {self.age}, Hobbies: {self.hobbies}, Profession: {self.profession}, Favorites: {self.favorites}"
    
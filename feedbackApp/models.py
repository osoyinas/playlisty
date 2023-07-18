from django.db import models

class Feedback(models.Model):
    score = models.IntegerField()
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    def __str__(self) -> str:
        return self.description

from django.db import models

# Create your models here.


class Poll(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return str(self.title)


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return str(self.text)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.question.poll.title} - {self.question.text} - {str(self.text)}"


class UserResponse(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.poll.title)


class Answer(models.Model):
    user_response = models.ForeignKey(UserResponse, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"user_id: {str(self.user_response.user_id)}"

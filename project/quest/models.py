from django.db import models

from Levenshtein import distance

class Level(models.Model):
    depth = models.IntegerField(unique=True)
    content = models.TextField()

    @property
    def content_length(self):
        return len(self.content)

    class Meta:
        ordering = ['depth']

class Code(models.Model):
    level = models.ForeignKey(Level, models.CASCADE)
    string = models.CharField(max_length=64)
    case_sensitive = models.BooleanField(default=False)
    max_edit_distance = models.PositiveSmallIntegerField(default=0)

    def is_match(self, user_input: str):
        right_code = self.string
        if self.case_sensitive:
            right_code, user_input = right_code.lower(), user_input.lower()
        return distance(right_code, user_input) <= self.max_edit_distance

    class Meta:
        ordering = ['level', 'string']
        constraints = [
            models.UniqueConstraint(
                fields=['level', 'string'], name='level, string'
            )
        ]


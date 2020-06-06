from django.db import models
from django.core import signing

from Levenshtein import distance

class Level(models.Model):
    depth = models.IntegerField(unique=True)
    title = models.CharField(max_length=128)
    content = models.TextField()

    signer = signing.Signer(sep=':', salt='load')

    @property
    def content_length(self):
        return len(self.content)

    def generate_signature(self):
        return self.signer.signature(self.depth)

    def is_signature_wrong(self, user_signature: str):
        try:
            self.signer.unsign(f'{self.depth}:{user_signature}')
        except signing.BadSignature: 
            return True
        return False

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


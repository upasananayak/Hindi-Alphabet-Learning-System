from django.db import models

class LetterImage(models.Model):
    order = models.IntegerField()
    letter_path = models.CharField(max_length=255)
    object_path = models.CharField(max_length=255, null=True, blank=True)
   

    def __str__(self):
        return f"{self.order} - {self.letter_path} - {self.object_path}"
    
class TestLetters(models.Model):
    order = models.IntegerField()
    letter_path = models.CharField(max_length=255)
    object_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.order} - {self.letter_path} - {self.object_path}"
    
class LetterTimestamp(models.Model):
    LETTER_TYPES = [
        ('vowel', 'Vowel'),
        ('consonant', 'Consonant'),
    ]

    letter = models.CharField(max_length=10)
    letter_type = models.CharField(max_length=10, choices=LETTER_TYPES)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    order = models.IntegerField()

    def __str__(self):
        return f"{self.letter} ({self.letter_type})"



class HindiLetter(models.Model):
    letter = models.CharField(max_length=10)
    transliteration = models.CharField(max_length=20)
    display_order = models.IntegerField()
    
    def __str__(self):
        return f"{self.letter} ({self.transliteration})"
    
    class Meta:
        ordering = ['display_order']

class Stroke(models.Model):
    letter = models.ForeignKey(HindiLetter, on_delete=models.CASCADE, related_name='strokes')
    stroke_order = models.IntegerField()
    description = models.CharField(max_length=100)
    svg_path = models.TextField()
    start_point_x = models.IntegerField()
    start_point_y = models.IntegerField()
    text_position_x = models.IntegerField()
    text_position_y = models.IntegerField()
    
    def __str__(self):
        return f"{self.letter.letter} - Stroke {self.stroke_order}: {self.description}"
    
    class Meta:
        ordering = ['letter', 'stroke_order']

class KeyPoint(models.Model):
    stroke = models.ForeignKey(Stroke, on_delete=models.CASCADE, related_name='key_points')
    point_order = models.IntegerField()
    x_coordinate = models.IntegerField()
    y_coordinate = models.IntegerField()
    
    def __str__(self):
        return f"{self.stroke.letter.letter} - Stroke {self.stroke.stroke_order} - Point {self.point_order}"
    
    class Meta:
        ordering = ['stroke', 'point_order']
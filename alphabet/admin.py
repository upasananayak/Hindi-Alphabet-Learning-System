from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
admin.site.register(LetterImage)
admin.site.register(TestLetters)
admin.site.register(LetterTimestamp)
admin.site.register(HindiLetter)
admin.site.register(Stroke)
admin.site.register(KeyPoint)
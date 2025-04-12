from django.core.management.base import BaseCommand
from alphabet.models import LetterImage

class Command(BaseCommand):
    help = 'Populate audio_path field based on order'

    def handle(self, *args, **kwargs):
        for letter_image in LetterImage.objects.all():
            letter_image.audio_path = f'static/letters_audio/{letter_image.order}.mp3'
            letter_image.save()
        self.stdout.write(self.style.SUCCESS('Successfully populated audio_path field'))
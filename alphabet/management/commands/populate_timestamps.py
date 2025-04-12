# filepath: your_app/management/commands/populate_letters.py
from django.core.management.base import BaseCommand
from alphabet.models import LetterTimestamp

class Command(BaseCommand):
    help = 'Populate the LetterTimestamp model with initial data'

    def handle(self, *args, **kwargs):
        data = [
            {'letter': 'अ', 'letter_type': 'vowel', 'start_time': 27, 'end_time': 44, 'order': 1},
            {'letter': 'आ', 'letter_type': 'vowel', 'start_time': 45, 'end_time': 68, 'order': 2},
            {'letter': 'उ', 'letter_type': 'vowel', 'start_time': 117, 'end_time': 133, 'order': 3},
            {'letter': 'ऊ', 'letter_type': 'vowel', 'start_time': 134, 'end_time': 158, 'order': 4},
            {'letter': 'ए', 'letter_type': 'vowel', 'start_time': 189, 'end_time': 208, 'order': 5},
            {'letter': 'ओ', 'letter_type': 'vowel', 'start_time': 236, 'end_time': 261, 'order': 6},
            {'letter': 'औ', 'letter_type': 'vowel', 'start_time': 262, 'end_time': 288, 'order': 7},
            {'letter': 'अं', 'letter_type': 'vowel', 'start_time': 289, 'end_time': 319, 'order': 8},
            {'letter': 'अः', 'letter_type': 'vowel', 'start_time': 322, 'end_time': 348, 'order': 9},
            {'letter': 'त', 'letter_type': 'consonant', 'start_time': 234, 'end_time': 240, 'order': 10},
            {'letter': 'र', 'letter_type': 'consonant', 'start_time': 366, 'end_time': 370, 'order': 11},
        ]

        for item in data:
            LetterTimestamp.objects.create(**item)

        self.stdout.write(self.style.SUCCESS('Successfully populated LetterTimestamp model'))
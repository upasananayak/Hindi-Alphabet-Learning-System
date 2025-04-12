# filepath: /home/upasana/221IT075/HCI/Project/alphabetLearning/alphabet/management/commands/populate_letters.py
import os
from django.core.management.base import BaseCommand
from alphabet.models import LetterImage, TestLetters

class Command(BaseCommand):
    help = 'Populate LetterImage and TestLetters models with data from static directories'

    def handle(self, *args, **kwargs):
        # Paths to the static directories
        learn_letters_path = 'alphabet/static/learn_letters'
        learn_objects_path = 'alphabet/static/learn_objects'
        test_letters_path = 'alphabet/static/test_letters'
        test_objects_path = 'alphabet/static/test_objects'

        # Populate LetterImage model
        for filename in os.listdir(learn_letters_path):
            if filename.endswith('.jpg'):
                order = int(filename.split('-')[0])
                letter_path = os.path.join(learn_letters_path, filename)
                object_path = os.path.join(learn_objects_path, filename)
                LetterImage.objects.create(order=order, letter_path=letter_path, object_path=object_path)

        # Populate TestLetters model
        for filename in os.listdir(test_letters_path):
            if filename.endswith('.jpg'):
                order = int(filename.split('-')[0])
                letter_path = os.path.join(test_letters_path, filename)
                object_path = os.path.join(test_objects_path, filename)
                TestLetters.objects.create(order=order, letter_path=letter_path, object_path=object_path)

        self.stdout.write(self.style.SUCCESS('Successfully populated LetterImage and TestLetters models'))
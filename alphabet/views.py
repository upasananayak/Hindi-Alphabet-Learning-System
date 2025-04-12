import os
import random
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from alphabet.models import HindiLetter, LetterImage, Stroke,TestLetters , LetterTimestamp

from django.http import JsonResponse

def index(request):
    return render(request, 'alphabet/home.html')
def dashboard(request):
    return render(request, 'alphabet/dashboard.html')
def learn(request):
    images = LetterImage.objects.order_by('order')
    context = {
        'image_list': [image.path for image in images]
    }
    return render(request, 'alphabet/learn.html', context)
def letter_matching(request):
    return render(request, 'alphabet/letterMatching.html')
def letters(request):
    images = LetterImage.objects.order_by('order')
    context = {
        'letters': images
    }
    return render(request, 'alphabet/letters.html', context)

# def learn_letter(request, order):
#     letter_image = get_object_or_404(LetterImage, order=order)

#     # Get next letter based on order or loop back to the first letter
#     next_letter_image = LetterImage.objects.filter(order__gt=order).order_by('order').first()
#     letter_data = get_object_or_404(LetterTimestamp, order=order)

#     if not next_letter_image:  
#         next_letter_image = LetterImage.objects.order_by('order').first()

#     next_letter_order = next_letter_image.order if next_letter_image else None
#     letter_obj = get_object_or_404(HindiLetter, display_order=order)
#     strokes = Stroke.objects.filter(letter=letter_obj).order_by('stroke_order')

#     stroke_data = [
#         {
#             "id": f"stroke{stroke.stroke_order}",
#             "description": stroke.description,
#             "start_point": [stroke.start_point_x, stroke.start_point_y],
#             "text_position": [stroke.text_position_x, stroke.text_position_y],
#             "key_points": [
#                 {"x": kp.x_coordinate, "y": kp.y_coordinate}
#                 for kp in stroke.key_points.all()
#             ],
#         }
#         for stroke in strokes
#     ]
#     context = {
#         'letter': letter_image.letter_path.split('/')[-1].split('-')[1],  # Extract letter from path
#         'letter_image': letter_image,
#         'next_letter': next_letter_order,
#         'letter_vid': letter_data.letter,
#         'letter_type': letter_data.letter_type,
#         'start_time': letter_data.start_time,
#         'end_time': letter_data.end_time,
#         'video_id': 'rmZKZg_9b9g' if letter_data.letter_type == 'vowel' else 'Yvb3we9HMFo',
#         "letter": letter_obj.letter,
#         "stroke_data": stroke_data,
#     }
#     return render(request, 'alphabet/learn_letter.html', context) 
def learn_letter(request, order):
    # Get the current letter image
    letter_image = get_object_or_404(LetterImage, order=order)
    
    # Get the next letter based on order or loop back to the first letter
    next_letter_image = LetterImage.objects.filter(order__gt=order).order_by('order').first()
    if not next_letter_image:  
        next_letter_image = LetterImage.objects.order_by('order').first()  # Loop back to the first letter

    next_letter_order = next_letter_image.order if next_letter_image else None

    # Get the current letter data
    letter_data = get_object_or_404(LetterTimestamp, order=order)

    # Get the Hindi letter object or loop back to the first one
    letter_obj = HindiLetter.objects.filter(display_order=order).first()
    if not letter_obj:
        letter_obj = HindiLetter.objects.order_by('display_order').first()

    # Get strokes for the current letter
    strokes = Stroke.objects.filter(letter=letter_obj).order_by('stroke_order')

    # Extract the current Hindi letter from the path
    current_letter = letter_image.letter_path.split('/')[-1].split('-')[1]
    print(current_letter)

    # Prepare stroke data
    stroke_data = [
        {
            "id": f"stroke{stroke.stroke_order}",
            "description": stroke.description,
            "start_point": [stroke.start_point_x, stroke.start_point_y],
            "text_position": [stroke.text_position_x, stroke.text_position_y],
            "key_points": [
                {"x": kp.x_coordinate, "y": kp.y_coordinate}
                for kp in stroke.key_points.all()
            ],
        }
        for stroke in strokes
    ]
    
    # Prepare context for the template
    context = {
        'letter': current_letter,  # Store the extracted letter here
        'letter_image': letter_image,
        'next_letter': next_letter_order,
        'letter_vid': letter_data.letter,
        'letter_type': letter_data.letter_type,
        'start_time': letter_data.start_time,
        'end_time': letter_data.end_time,
        'video_id': 'rmZKZg_9b9g' if letter_data.letter_type == 'vowel' else 'Yvb3we9HMFo',
        'hindi_letter': letter_obj.letter,  # Renamed to avoid duplicate key
        'stroke_data': stroke_data,
    }
    
    return render(request, 'alphabet/learn_letter.html', context)

def test(request):
    flask_url = "http://127.0.0.1:8080"  # Update this to dynamically determine the Flask URL if needed
    return render(request, 'alphabet/test.html', {'flask_url': flask_url})

def redirect_to_flask(request):
    return redirect("http://127.0.0.1:8080/")

def test_letter(request, order):
    letter_image = get_object_or_404(TestLetters, order=order)
    next_letter_image = TestLetters.objects.filter(order__gt=order).order_by('order').first()
    if not next_letter_image:  
        next_letter_image = TestLetters.objects.order_by('order').first()

    next_letter_order = next_letter_image.order if next_letter_image else None
    context = {
        'letter': letter_image.letter_path.split('/')[-1].split('-')[1],  # Extract letter from path
        'letter_image': letter_image,
        'next_letter': next_letter_order,
    }
    return render(request, 'alphabet/test_letter.html', context)

def get_image_paths(request, order):
    letter_image = get_object_or_404(TestLetters, order=order)

    return JsonResponse({
        'letter_path': f"http://127.0.0.1:8000/static/{letter_image.letter_path}",
        'object_path': f"http://127.0.0.1:8000/static/{letter_image.object_path}" if letter_image.object_path else None
    })

def video_animation_view(request):
    letters = LetterTimestamp.objects.all().order_by('order')
    return render(request, 'alphabet/videoAnimation1.html', {'letters': letters})

def stroke_view(request,order):
    return render(request, 'alphabet/integrated.html')
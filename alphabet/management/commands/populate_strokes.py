import os
import json
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

from alphabet.models import HindiLetter, Stroke, KeyPoint

# Clear existing data
HindiLetter.objects.all().delete()

# Letter data from the HTML file
letter_data = {
    "अ": [
        { 
        "id": "stroke1", 
        "d": "M70,50 A50,35 0 1,1 70,120", 
        "dot": [70,50], 
        "text": [50,60],
        "description": "Top curved stroke",
        "keyPoints": [[70, 50], [90, 65], [100, 85], [90, 105], [70, 120]]
        },
        { 
        "id": "stroke2", 
        "d": "M70,120 A50,35 0 1,1 70,190", 
        "dot": [70,120], 
        "text": [85,150],
        "description": "Bottom curved stroke",
        "keyPoints": [[70, 120], [90, 140], [100, 155], [90, 170], [70, 190]]
        },
        { 
        "id": "stroke3", 
        "d": "M70,120 H140", 
        "dot": [70,120], 
        "text": [100,110],
        "description": "Horizontal middle stroke",
        "keyPoints": [[70, 120], [105, 120], [140, 120]]
        },
        { 
        "id": "stroke4", 
        "d": "M140,50 V180", 
        "dot": [140,50], 
        "text": [145,40],
        "description": "Vertical right stroke",
        "keyPoints": [[140, 50], [140, 115], [140, 180]]
        },
        { 
        "id": "stroke5", 
        "d": "M110,50 H170", 
        "dot": [110,50], 
        "text": [120,40],
        "description": "Top horizontal stroke",
        "keyPoints": [[110, 50], [140, 50], [170, 50]]
        }
    ],
    
    "आ": [
        { 
        "id": "stroke1", 
        "d": "M70,50 A50,35 0 1,1 70,120", 
        "dot": [70,50], 
        "text": [50,60],
        "description": "Top curved stroke",
        "keyPoints": [[70, 50], [90, 65], [100, 85], [90, 105], [70, 120]]
        },
        { 
        "id": "stroke2", 
        "d": "M70,120 A50,35 0 1,1 70,190", 
        "dot": [70,120], 
        "text": [85,150],
        "description": "Bottom curved stroke",
        "keyPoints": [[70, 120], [90, 140], [100, 155], [90, 170], [70, 190]]
        },
        { 
        "id": "stroke3", 
        "d": "M70,120 H140", 
        "dot": [70,120], 
        "text": [100,110],
        "description": "Horizontal middle stroke",
        "keyPoints": [[70, 120], [105, 120], [140, 120]]
        },
        { 
        "id": "stroke4", 
        "d": "M140,50 V180", 
        "dot": [140,50], 
        "text": [145,40],
        "description": "Vertical first right stroke",
        "keyPoints": [[140, 50], [140, 115], [140, 180]]
        },
        { 
        "id": "stroke5", 
        "d": "M110,50 H170", 
        "dot": [110,50], 
        "text": [120,40],
        "description": "Top horizontal stroke",
        "keyPoints": [[110, 50], [140, 50], [170, 50]]
        },
        { 
        "id": "stroke6", 
        "d": "M160,50 V180", 
        "dot": [160,50], 
        "text": [180,40],
        "description": "Vertical second right stroke",
        "keyPoints": [[160, 50], [160, 115], [160, 180]]
        }
    ],
    
    "उ": [
        { 
        "id": "stroke1", 
        "d": "M70,50 A50,35 0 1,1 70,120", 
        "dot": [70,50], 
        "text": [60,70],
        "description": "Top curved stroke",
        "keyPoints": [[70, 50], [90, 65], [100, 85], [90, 105], [70, 120]]
        },
        { 
        "id": "stroke2", 
        "d": "M70,120 A50,35 0 1,1 70,190", 
        "dot": [70,120], 
        "text": [85,150],
        "description": "Bottom curved stroke",
        "keyPoints": [[70, 120], [90, 140], [100, 155], [90, 170], [70, 190]]
        },
        { 
        "id": "stroke3", 
        "d": "M50,50 H170", 
        "dot": [50,50], 
        "text": [50,40],
        "description": "Top horizontal stroke",
        "keyPoints": [[50, 50], [110, 50], [170, 50]]
        }
    ],
    
    "ऊ": [
        { 
            "id": "stroke1", 
            "d": "M70,50 A50,35 0 1,1 70,120", 
            "dot": [70,50], 
            "text": [60,70],
            "description": "Top curved stroke",
            "keyPoints": [[70, 50], [90, 65], [100, 85], [90, 105], [70, 120]]
        },
        { 
            "id": "stroke2", 
            "d": "M70,120 A50,35 0 1,1 70,190", 
            "dot": [70,120], 
            "text": [85,150],
            "description": "Bottom curved stroke",
            "keyPoints": [[70, 120], [90, 140], [100, 155], [90, 170], [70, 190]]
        },
        { 
            "id": "stroke3", 
            "d": "M50,50 H170", 
            "dot": [50,50], 
            "text": [50,40],
            "description": "Top horizontal stroke",
            "keyPoints": [[50, 50], [110, 50], [170, 50]]
        },
        { 
            "id": "stroke4", 
            "d": "M70,120 A45,45 0 0,1 130,180", 
            "dot": [70,120], 
            "text": [100,180],
            "description": "Bottom right curved extension",
            "keyPoints": [[70, 120], [85, 140], [100, 160], [115, 175], [130, 180]]
        }
    ],
    "ए": [
        { 
        "id": "stroke1", 
        "d": "M130,50 V110", 
        "dot": [130,50], 
        "text": [145,40],
        "description": "Vertical left stroke",
        "keyPoints": [[130, 50], [130, 80], [130, 110]]
        },
        { 
        "id": "stroke2", 
        "d": "M130,110 L200,170", 
        "dot": [130,110], 
        "text": [140,130],
        "description": "Diagonal stroke",
        "keyPoints": [[130, 110], [165, 140], [200, 170]]
        },
        { 
        "id": "stroke3", 
        "d": "M190,50 V80", 
        "dot": [190,50], 
        "text": [200,40],
        "description": "Vertical right stroke",
        "keyPoints": [[190, 50], [190, 65], [190, 80]]
        },
        { 
        "id": "stroke4", 
        "d": "M190,80 L175,100", 
        "dot": [190,80], 
        "text": [200,80],
        "description": "Small diagonal stroke",
        "keyPoints": [[190, 80], [182, 90], [175, 100]]
        },
        { 
        "id": "stroke5", 
        "d": "M110,50 H250", 
        "dot": [110,50], 
        "text": [120,40],
        "description": "Top horizontal stroke",
        "keyPoints": [[110, 50], [180, 50], [250, 50]]
        }
    ],
    
    "ओ": [
        { 
        "id": "stroke1", 
        "d": "M70,50 A50,35 0 1,1 70,120", 
        "dot": [70,50], 
        "text": [50,60],
        "description": "Top curved stroke",
        "keyPoints": [[70, 50], [90, 65], [100, 85], [90, 105], [70, 120]]
        },
        { 
        "id": "stroke2", 
        "d": "M70,120 A50,35 0 1,1 70,190", 
        "dot": [70,120], 
        "text": [85,150],
        "description": "Bottom curved stroke",
        "keyPoints": [[70, 120], [90, 140], [100, 155], [90, 170], [70, 190]]
        },
        { 
        "id": "stroke3", 
        "d": "M70,120 H140", 
        "dot": [70,120], 
        "text": [100,110],
        "description": "Horizontal middle stroke",
        "keyPoints": [[70, 120], [105, 120], [140, 120]]
        },
        { 
        "id": "stroke4", 
        "d": "M140,50 V180", 
        "dot": [140,50], 
        "text": [145,40],
        "description": "Vertical first right stroke", 
        "keyPoints": [[140, 50], [140, 115], [140, 180]]
        },
        { 
        "id": "stroke5", 
        "d": "M110,50 H170", 
        "dot": [110,50], 
        "text": [120,40],
        "description": "Top horizontal stroke",
        "keyPoints": [[110, 50], [140, 50], [170, 50]]
        },
        { 
        "id": "stroke6", 
        "d": "M160,50 V180", 
        "dot": [160,50], 
        "text": [170,40],
        "description": "Vertical second right stroke",
        "keyPoints": [[160, 50], [160, 115], [160, 180]]
        },
        { 
        "id": "stroke7", 
        "d": "M160,50 L100,20", 
        "dot": [160,50], 
        "text": [160,40],
        "description": "Diagonal top stroke",
        "keyPoints": [[160, 50], [130, 35], [100, 20]]
        }
    ],
    
    "औ": [
        { 
        "id": "stroke1", 
        "d": "M70,50 A50,35 0 1,1 70,120", 
        "dot": [70,50], 
        "text": [50,60],
        "description": "Top curved stroke",
        "keyPoints": [[70, 50], [90, 65], [100, 85], [90, 105], [70, 120]]
        },
        { 
        "id": "stroke2", 
        "d": "M70,120 A50,35 0 1,1 70,190", 
        "dot": [70,120], 
        "text": [85,150],
        "description": "Bottom curved stroke",
        "keyPoints": [[70, 120], [90, 140], [100, 155], [90, 170], [70, 190]]
        },
        { 
        "id": "stroke3", 
        "d": "M70,120 H140", 
        "dot": [70,120], 
        "text": [100,110],
        "description": "Horizontal middle stroke",
        "keyPoints": [[70, 120], [105, 120], [140, 120]]
        },
        { 
        "id": "stroke4", 
        "d": "M140,50 V180", 
        "dot": [140,50], 
        "text": [145,40],
        "description": "Vertical first right stroke",
        "keyPoints": [[140, 50], [140, 115], [140, 180]]
        },
        { 
        "id": "stroke5", 
        "d": "M110,50 H170", 
        "dot": [110,50], 
        "text": [120,40],
        "description": "Top horizontal stroke",
        "keyPoints": [[110, 50], [140, 50], [170, 50]]
        },
        { 
        "id": "stroke6", 
        "d": "M160,50 V180", 
        "dot": [160,50], 
        "text": [170,40],
        "description": "Vertical second right stroke",
        "keyPoints": [[160, 50], [160, 115], [160, 180]]
        },
        { 
        "id": "stroke7", 
        "d": "M160,50 L100,20", 
        "dot": [160,50], 
        "text": [160,40],
        "description": "First diagonal top stroke",
        "keyPoints": [[160, 50], [130, 35], [100, 20]]
        },
        { 
        "id": "stroke8", 
        "d": "M160,50 L130,20", 
        "dot": [160,50], 
        "text": [150,30],
        "description": "Second diagonal top stroke",
        "keyPoints": [[160, 50], [145, 35], [130, 20]]
        }
    ],
    
    "अं": [
        { 
        "id": "stroke1", 
        "d": "M70,50 A50,35 0 1,1 70,120", 
        "dot": [70,50], 
        "text": [50,60],
        "description": "Top curved stroke",
        "keyPoints": [[70, 50], [90, 65], [100, 85], [90, 105], [70, 120]]
        },
        { 
        "id": "stroke2", 
        "d": "M70,120 A50,35 0 1,1 70,190", 
        "dot": [70,120], 
        "text": [85,150],
        "description": "Bottom curved stroke",
        "keyPoints": [[70, 120], [90, 140], [100, 155], [90, 170], [70, 190]]
        },
        { 
        "id": "stroke3", 
        "d": "M70,120 H140", 
        "dot": [70,120], 
        "text": [100,110],
        "description": "Horizontal middle stroke",
        "keyPoints": [[70, 120], [105, 120], [140, 120]]
        },
        { 
        "id": "stroke4", 
        "d": "M140,50 V180", 
        "dot": [140,50], 
        "text": [145,40],
        "description": "Vertical right stroke",
        "keyPoints": [[140, 50], [140, 115], [140, 180]]
        },
        { 
        "id": "stroke5", 
        "d": "M110,50 H170", 
        "dot": [110,50], 
        "text": [120,40],
        "description": "Top horizontal stroke",
        "keyPoints": [[110, 50], [140, 50], [170, 50]]
        },
        { 
        "id": "stroke6", 
        "d": "M125,25 A10,10 0 1,1 135,25", 
        "dot": [130,25], 
        "text": [130,15],
        "description": "Anusvar dot",
        "keyPoints": [[125, 25], [130, 15], [135, 25], [130, 35], [125, 25]]
        } 
    ],
    
    "अः": [
        { 
        "id": "stroke1", 
        "d": "M70,50 A50,35 0 1,1 70,120", 
        "dot": [70,50], 
        "text": [50,60],
        "description": "Top curved stroke",
        "keyPoints": [[70, 50], [90, 65], [100, 85], [90, 105], [70, 120]]
        },
        { 
        "id": "stroke2", 
        "d": "M70,120 A50,35 0 1,1 70,190", 
        "dot": [70,120], 
        "text": [85,150],
        "description": "Bottom curved stroke",
        "keyPoints": [[70, 120], [90, 140], [100, 155], [90, 170], [70, 190]]
        },
        { 
        "id": "stroke3", 
        "d": "M70,120 H140", 
        "dot": [70,120], 
        "text": [100,110],
        "description": "Horizontal middle stroke",
        "keyPoints": [[70, 120], [105, 120], [140, 120]]
        },
        { 
        "id": "stroke4", 
        "d": "M140,50 V180", 
        "dot": [140,50], 
        "text": [145,40],
        "description": "Vertical right stroke",
        "keyPoints": [[140, 50], [140, 115], [140, 180]]
        },
        { 
        "id": "stroke5", 
        "d": "M110,50 H170", 
        "dot": [110,50], 
        "text": [120,40],
        "description": "Top horizontal stroke",
        "keyPoints": [[110, 50], [140, 50], [170, 50]]
        },
        { 
        "id": "stroke6", 
        "d": "M160,170 A5,5 0 1,1 165,170", 
        "dot": [160,170], 
        "text": [155,165],
        "description": "Upper visarga dot",
        "keyPoints": [[160, 170], [162.5, 165], [165, 170], [162.5, 175], [160, 170]]
        },
        { 
        "id": "stroke7", 
        "d": "M160,185 A5,5 0 1,1 165,185", 
        "dot": [160,185], 
        "text": [155,200],
        "description": "Lower visarga dot",
        "keyPoints": [[160, 185], [162.5, 180], [165, 185], [162.5, 190], [160, 185]]
        }
    ],
    
    "त": [
        { 
        "id": "stroke1", 
        "d": "M150,30 L150,170", 
        "dot": [150,30], 
        "text": [155,25],
        "description": "Vertical stroke",
        "keyPoints": [[150, 30], [150, 100], [150, 170]]
        },
        { 
        "id": "stroke2", 
        "d": "M150,100 Q90,130 80,170", 
        "dot": [150,100], 
        "text": [115,65],
        "description": "Curved stroke",
        "keyPoints": [[150, 100], [120, 120], [100, 140], [80, 170]]
        },
        { 
        "id": "stroke3", 
        "d": "M50,30 H300", 
        "dot": [50,30], 
        "text": [35,25],
        "description": "Top horizontal stroke",
        "keyPoints": [[50, 30], [175, 30], [300, 30]]
        }
    ],
    
    "र": [
        { 
        "id": "stroke1", 
        "d": "M100,30 A100,50 0 0,1 100,100", 
        "dot": [100,30], 
        "text": [105,25],
        "description": "Curved top stroke",
        "keyPoints": [[100, 30], [120, 50], [120, 80], [100, 100]]
        },
        { 
        "id": "stroke2", 
        "d": "M100,100 L130,150", 
        "dot": [100,100], 
        "text": [110,95],
        "description": "Diagonal stroke",
        "keyPoints": [[100, 100], [115, 125], [130, 150]]
        },
        { 
        "id": "stroke3", 
        "d": "M50,30 H300", 
        "dot": [50,30], 
        "text": [55,45],
        "description": "Top horizontal stroke",
        "keyPoints": [[50, 30], [175, 30], [300, 30]]
        }
    ]
}

# Map of letters to transliterations from the select element options
letter_transliterations = {
    "अ": "a",
    "आ": "aa",
    "उ": "u",
    "ऊ": "oo",
    "ओ": "o",
    "औ": "au",
    "ए": "e",
    "अं": "anusvara",
    "अः": "visarga",
    "त": "ta",
    "र": "ra"
}

# Populate the database
for i, (letter_char, strokes) in enumerate(letter_data.items()):
    # Create the Hindi letter
    hindi_letter = HindiLetter.objects.create(
        letter=letter_char,
        transliteration=letter_transliterations[letter_char],
        display_order=i
    )
    
    print(f"Created letter: {hindi_letter}")
    
    # Create strokes for this letter
    for j, stroke_data in enumerate(strokes):
        stroke = Stroke.objects.create(
            letter=hindi_letter,
            stroke_order=j + 1,
            description=stroke_data["description"],
            svg_path=stroke_data["d"],
            start_point_x=stroke_data["dot"][0],
            start_point_y=stroke_data["dot"][1],
            text_position_x=stroke_data["text"][0],
            text_position_y=stroke_data["text"][1]
        )
        
        print(f"  Created stroke: {stroke}")
        
        # Create key points for this stroke
        for k, key_point in enumerate(stroke_data["keyPoints"]):
            point = KeyPoint.objects.create(
                stroke=stroke,
                point_order=k + 1,
                x_coordinate=key_point[0],
                y_coordinate=key_point[1]
            )
            
            print(f"    Created key point: {point}")

print("Database population complete!")
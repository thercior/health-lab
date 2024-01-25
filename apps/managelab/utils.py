from django.conf import settings
from django.template.loader import render_to_string
from io import BytesIO
from random import choice, shuffle
from weasyprint import HTML
import os, string


def random_pass_generate(size):
    specials_characters = string.punctuation
    characters = string.ascii_letters
    numbers_list = string.digits
        
    qtd = size // 3
    surplus = (size - (qtd * 3)) if size % 3 != 0 else 0
        
    letters = ''.join([choice(characters) for char in range(0, qtd + surplus)])
    numbers = ''.join([choice(numbers_list) for char in range(0, qtd)])
    specials_char = ''.join([choice(specials_characters) for char in range(0, qtd )])
    
    random_password = list(letters + numbers + specials_char)
    shuffle(random_password)
    
    return ''.join(random_password)
    
def pdf_pass_exams(exam, client, random_password):
    path_template = os.path.join(settings.BASE_DIR, 'templates/Partials/exam_pass.html')
    template_render = render_to_string(
        path_template,
        {
            'exam': exam,
            'client': client,
            'random_password': random_password,
        }
    )
    
    path_output = BytesIO()
    HTML(string=template_render).write_pdf(path_output)
    path_output.seek(0)
    
    return path_output
    
    

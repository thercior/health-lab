from random import choice, shuffle
import string


def random_pass_generate(size):
    specials_characters = string.punctuation
    characters = string.ascii_letters
    numbers_list = string.digits
        
    qtd = size // 3
    surplus = (size - (qtd*2)) if size % 3 != 0 else 0
        
    letters = ''.join([choice(characters) for char in range(0, qtd + surplus)])
    numbers = ''.join([choice(numbers_list) for char in range(0, qtd)])
    specials_char = ''.join([choice(specials_characters) for char in range(0, qtd )])
    
    random_password = list(letters + numbers + specials_char)
    shuffle(random_password)
    
    return ''.join(random_password)
    
    
    

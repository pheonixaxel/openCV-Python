import os

def generate_negative_description_file():
    with open('neg.txt', 'w') as f:
        for img in os.listdir('negative'):
            f.write('negative/' + img + '\n')
from random import randint
from faker import Faker

def rand_ratio():
    return randint(840,900), randint(473,573)


fake = Faker('pt-BR')

def make_recipe():
    return {
        'id':fake.unique.random_number(digits=3, fix_len=True),
        'title': fake.sentence(nb_words=6),
        'description': fake.sentence(nb_words=12),
        'preparation_time': fake.random_number(digits=2, fix_len=True),
        'preparation_time_unit': 'Minutos',
        'servings': fake.random_number(digits=2, fix_len=True),
        'servings_unit': 'Porções',
        'preparation_steps': fake.text(3000),
        'created_at_date': fake.date_time().now().strftime("%d/%m/%Y"),
        'created_at_hour': fake.date_time().now().strftime("%H:%M"),
        'author': {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        },
        'category': {
            'name': fake.word()
        },
        'cover': {
            'url': 'https://loremflickr.com/%s/%s/cook, food' % rand_ratio(),
        }

    }

if __name__ =='__main__':
    teste = make_recipe()
    print(teste['created_at_date'])
    print(teste['created_at_hour'])
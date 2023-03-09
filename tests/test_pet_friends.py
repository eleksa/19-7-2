from settings import e_mail, pass_word
from api import PetFriends
import os

pf = PetFriends()


def test_get_key(email=e_mail, password=pass_word):
    """Проверяем что для зарегистрированного пользователя получаем api ключ при указании корректных данных."""

    code, output = pf.get_token(email, password)

    assert code == 200
    assert 'key' in output


def test_not_get_key_with_invalid_data(email='', password=''):
    """Проверяем что сервис не вернет ключ api при использовании некорректных данных."""

    code, output = pf.get_token(email, password)

    assert code == 403
    assert 'key' not in output


def test_get_list_all_pets_with_valid_input_data(filter=''):
    """Проверяем что запрос возвращает список всех питомцев при использовании полученного ключа."""

    api_key = pf.get_token(e_mail, pass_word)
    code, all_pet_list = pf.get_pet_list(api_key[1], filter=filter)

    assert code == 200
    assert len(all_pet_list.get('pets')) > 0


def test_add_new_pet_with_valid_input_data(name='Гусак Гаврилыч', animal_type='Очень важный гусь', age='10',
                                           pet_photo='media\important_goose.jpg'):
    """Проверяем возможность добавления на сервер нового питомца с фото."""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    api_key = pf.get_token(e_mail, pass_word)
    code, new_pet = pf.add_new_pet(api_key[1], name=name, animal_type=animal_type, age=age, pet_photo=pet_photo)

    assert code == 200
    assert new_pet.get('name') == name


def test_update_new_data_pet(name='Мартин', animal_type='Домашний гусь', age='7'):
    """Проверяем возможность изменения у питомца основных данных"""

    api_key = pf.get_token(e_mail, pass_word)
    my_pet_list = pf.get_pet_list(api_key[1], 'my_pets')

    if len(my_pet_list[1].get('pets')) > 0:

        code, upd_pet = pf.update_info_pet(api_key[1], my_pet_list[1].get('pets')[0].get('id'), name, animal_type, age)

        assert code == 200
        assert upd_pet.get('name') == name

    else:
        raise Exception("Добавленные питомцы отсутствуют")


def test_delete_pet():
    """Проверяем возможность удаления питомца"""

    api_key = pf.get_token(e_mail, pass_word)
    my_pet_list = pf.get_pet_list(api_key[1], 'my_pets')

    if len(my_pet_list[1].get('pets')) == 0:

        pf.add_new_pet(api_key[1], name='Мартин', animal_type='Гусь', age='7', pet_photo='media\important_goose.jpg')
        my_pet_list = pf.get_pet_list(api_key[1], 'my_pets')

    pet_id = my_pet_list[1].get('pets')[0].get('id')
    code = pf.delete_pet(api_key[1], pet_id)
    my_pet_list = pf.get_pet_list(api_key[1], 'my_pets')

    assert code[0] == 200
    assert pet_id not in my_pet_list[1].values()


def test_add_new_pet_with_valid_input_data_without_photo(name='Гусак Гаврилыч', animal_type='Гусь', age='5'):
    """Проверяем возможность добавления питомца без фото"""

    api_key = pf.get_token(e_mail, pass_word)
    code, add_new_pet_without_photo = pf.add_new_pet_no_photo(api_key[1], name, animal_type, age)

    assert code == 200
    assert add_new_pet_without_photo.get('name') == name


def test_add_photo_to_pet(pet_photo='media\spy_goose.jpg'):
    """Проверяем возможность добавления фото питомцу"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    api_key = pf.get_token(e_mail, pass_word)
    my_pet_list = pf.get_pet_list(api_key[1], 'my_pets')

    if len(my_pet_list[1].get('pets')) > 0:

        pet_id = my_pet_list[1].get('pets')[0].get('id')
        code, add_photo = pf.add_photo_pet(api_key[1], pet_id, pet_photo)
        my_pet_list = pf.get_pet_list(api_key[1], 'my_pets')

        assert code == 200
        assert add_photo.get('pet_photo') == my_pet_list[1].get('pets')[0].get('pet_photo')

    else:
        raise Exception("Добавленные питомцы отсутствуют")


def test_add_new_pet_with_negative_age(name='Гусак Гаврилыч', animal_type='Гусь', age='-5'):
    """Проверяем возможность добавления питомца с отрицательным возрастом.
    Тест не будет пройден если питомец будет успешно добавлен."""

    api_key = pf.get_token(e_mail, pass_word)
    add_new_pet_without_photo = pf.add_new_pet_no_photo(api_key[1], name, animal_type, age)

    assert age not in add_new_pet_without_photo[1].get('age'), \
        'Питомец добавлен с отрицательным значение в поле возраст'


def test_add_new_pet_with_null_data(name=False, animal_type=False, age=False):
    """Проверяем возможность добавления питомца со значениями отличными от строковых.
    Тест не будет пройден если питомец будет успешно добавлен."""

    api_key = pf.get_token(e_mail, pass_word)
    add_new_pet_null = pf.add_new_pet_no_photo(api_key[1], name, animal_type, age)

    assert str(name) not in add_new_pet_null[1].get('name'), 'Питомец добавлен со значениями типа Boolean'

import requests
import json


class PetFriends:
    """Класс для работы с веб-приложением PetFriends (https://petfriends.skillfactory.ru)"""

    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_token(self, email: str, password: str) -> tuple:
        """Метод для получения уникального ключа пользователя по указанным email и паролю.
        Метод возвращает статус запроса и результат в формате JSON.

        :param email: Email зарегистрированного пользователя.
        :param password: Пароль пользователя.
        :return: Http статус код, уникальный api ключ пользователя.
        """

        func_headers = {
            'email': email,
            'password': password,
            'accept': 'application/json'
        }

        get_token_response = requests.get(url=f'{self.base_url}/api/key', headers=func_headers)

        status_code = get_token_response.status_code
        if get_token_response.status_code == 200 \
                and 'application/json' in get_token_response.headers.get('Content-Type'):
            message = get_token_response.json()
        else:
            message = get_token_response.text

        return status_code, message

    def get_pet_list(self, auth_key: json, filter: str = '') -> tuple:
        """Метод возвращает результат запроса к серверу в формате JSON со списком найденных питомцев согласно
        заданному фильтру и код запроса. Фильтр может принимать пустое значение (по умолчанию) для вывода всех
        питомцев, или 'my_pets' для вывода списка только своих питомцев.

        :param auth_key: Уникальный api ключ пользователя.
        :param filter: Пользовательский фильтр.
        :return: Http статус код, отфильтрованный список питомцев.
        """

        func_headers = {
            'accept': 'application/json',
            'auth_key': auth_key.get('key')
        }

        func_filters = {
            'filter': filter
        }

        pet_list_response = requests.get(url=f'{self.base_url}/api/pets', headers=func_headers, params=func_filters)

        status_code = pet_list_response.status_code
        if pet_list_response.status_code == 200 and 'application/json' in pet_list_response.headers.get('Content-Type'):
            message = pet_list_response.json()
        else:
            message = pet_list_response.text

        return status_code, message

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> tuple:
        """Метод позволяет добавить на сервер данные о новом питомце, а также установить для него изображение.
        В ответе возвращаются код запроса и данные о добавленном питомце в формате JSON.

        :param auth_key: Уникальный api ключ пользователя.
        :param name: Имя питомца.
        :param animal_type: Вид питомца.
        :param age: Возраст питомца.
        :param pet_photo: Фото питомца.
        :return: Http статус код, данные питомца в формате JSON.
        """

        func_headers = {
            'accept': 'application/json',
            'auth_key': auth_key.get('key')
        }

        func_data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        with open(pet_photo, 'rb') as bytes_image:
            photo = {
                'pet_photo': (
                    pet_photo, bytes_image, 'image/jpeg'
                )
            }
            new_pet_response = requests.post(url=f'{self.base_url}/api/pets', headers=func_headers,
                                             data=func_data, files=photo)

            status_code = new_pet_response.status_code
            if new_pet_response.status_code == 200 and 'application/json' in new_pet_response.headers.get(
                    'Content-Type'):
                message = new_pet_response.json()
            else:
                message = new_pet_response.text

            return status_code, message

    def add_new_pet_no_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> tuple:
        """Метод позволяет добавить питомца без фото и возвращает результат в формате JSON с данными
        добавленного питомца и код запроса.

        :param auth_key: Уникальный api ключ пользователя.
        :param name: Имя питомца.
        :param animal_type: Вид питомца.
        :param age: Возраст питомца.
        :return: Http статус код, данные питомца в формате JSON.
        """

        func_headers = {
            'accept': 'application/json',
            'auth_key': auth_key.get('key')
        }

        func_data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        add_pet_response = requests.post(url=f'{self.base_url}/api/create_pet_simple', headers=func_headers,
                                         json=func_data)

        status_code = add_pet_response.status_code
        if add_pet_response.status_code == 200 and 'application/json' in add_pet_response.headers.get('Content-Type'):
            message = add_pet_response.json()
        else:
            message = add_pet_response.text

        return status_code, message

    def add_photo_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> tuple:
        """Метод позволяет изменить фото у добавленного питомца. Возвращает ответ на запрос в формате JSON с данными
        питомца и код запроса.

        :param auth_key: Уникальный api ключ пользователя.
        :param pet_id: Уникальный идентификатор питомца.
        :param pet_photo: Путь до файла с изображением.
        :return: Http статус код, данные питомца в формате JSON.
        """

        func_headers = {
            'accept': 'application/json',
            'auth_key': auth_key.get('key')
        }

        with open(pet_photo, 'rb') as bytes_image:
            photo = {
                'pet_photo': (
                    pet_photo, bytes_image, 'image/jpeg'
                )
            }

            add_photo_response = requests.post(url=f'{self.base_url}/api/pets/set_photo/{pet_id}',
                                               headers=func_headers, files=photo)

        if add_photo_response.status_code == 200 and \
                'application/json' in add_photo_response.headers.get('Content-Type'):
            message = add_photo_response.json()
            status_code = add_photo_response.status_code
        else:
            message = add_photo_response.text
            status_code = add_photo_response.status_code

        return status_code, message

    def update_info_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> tuple:
        """Метод позволяет изменить имя, вид, возраст питомца по его идентификатору.
        В ответе возвращаются код запроса и данные питомца в формате JSON.

        :param auth_key: Уникальный api ключ пользователя.
        :param pet_id: Уникальный идентификатор питомца.
        :param name: Имя питомца.
        :param animal_type: Вид питомца.
        :param age: Возраст питомца.
        :return: Http статус код, измененные данные питомца в формате JSON.
        """

        func_headers = {
            'accept': 'application/json',
            'auth_key': auth_key.get('key')
        }

        func_data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        update_pet_response = requests.put(url=f'{self.base_url}/api/pets/{pet_id}', headers=func_headers,
                                           data=func_data)

        if update_pet_response.status_code == 200 and \
                'application/json' in update_pet_response.headers.get('Content-Type'):
            message = update_pet_response.json()
            status_code = update_pet_response.status_code
        else:
            message = update_pet_response.text
            status_code = update_pet_response.status_code

        return status_code, message

    def delete_pet(self, auth_key: json, pet_id: str) -> tuple:
        """Метод позволяет удалить питомца по его уникальному идентификатору.

        :param auth_key: Уникальный api ключ пользователя.
        :param pet_id: Уникальный идентификатор питомца.
        :return: Http статус код
        """

        func_headers = {
            'accept': 'application/json',
            'auth_key': auth_key.get('key')
        }

        delete_pet_response = requests.delete(url=f'{self.base_url}/api/pets/{pet_id}', headers=func_headers)

        if delete_pet_response.status_code == 200 and \
                'application/json' in delete_pet_response.headers.get('Content-Type'):
            message = type(delete_pet_response.json())
            status_code = delete_pet_response.status_code
        else:
            message = delete_pet_response.text
            status_code = delete_pet_response.status_code

        return status_code, message
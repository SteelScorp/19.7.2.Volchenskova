from api import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что можно получить api_key, указав валидные данные почты и пароля """

    status, result = pf.get_api_key(email, password)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=""):
    """Проверяем, что можно получить список питомцев"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Запрашиваем список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result["pets"]) > 0

def test_add_new_pet_with_valid_data(name='Лапуля', animal_type='терьер',
                                     age='1', pet_photo='images/Dog.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Рекс", "овчарка", "2", "images/Dog2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Ушастик', animal_type='эртерьер', age=2):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиcок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Тест №1. Добавление питомца с корректными данными без фото.
def test_add_new_pet_without_photo_with_valid_data(name='Торетто', animal_type='акита',
                                     age='1'):

     # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# Тест №2. Добавление фото питомца.
def test_add_photo_of_pet(pet_photo='images/Dog3.jpg'):

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200 и фото добавлено
        assert status == 200
        assert 'pet_photo' in result

# Тест №3. Ввод неверного email при запросе Api key.
def test_get_api_key_for_not_valid_user(email=not_valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    # Проверяем что статус ответа = 403 и ключ не получен
    assert status == 403
    assert 'key' not in result

# Тест №4. Ввод неверного password при запросе Api key.
def test_get_api_key_for_not_valid_user(email=valid_email, password=not_valid_password):
    status, result = pf.get_api_key(email, password)

    # Проверяем что статус ответа = 403 и ключ не получен
    assert status == 403
    assert 'key' not in result

# Тест №5. БАГ. Добавление питомца с некорректными данными.
def test_add_new_pet_with_not_valid_data(name='', animal_type='123',
                                     age='asd', pet_photo='images/Dog.jpg'):

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем что статус ответа = 400 и питомец не добавился на сайт
    # Баг, статус 200 и питомец с некорректными данными добавлен в список питомцев
    assert status == 400
    assert 'name' not in result

#Тест №6. БАГ. Удаление питомца с некорректным ID.
def test_delete_pet_not_valid_ID():

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = '1a2s3d4567'
    status, result = pf.delete_pet(auth_key, pet_id)

    # Проверяем что статус ответа = 403.
    # Баг, статус 200.
    assert status == 403
    assert pet_id not in result

#Тест №7. БАГ. Добавление питомца с пустыми данными без фото.
def test_add_new_pet_without_photo_with_not_valid_data(name='', animal_type='',
                                     age=''):

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Проверяем что статус ответа = 400.
    # Баг, статус 200 и питомец с пустыми данными добавлен в список питомцев
    assert status == 400
    assert 'name' not in result

# Тест №8. БАГ. Добавление фото питомца некорректного формата.
def test_add_photo_of_pet_incorrect_format(pet_photo='images/DOG6.webp'):

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Проверяем что статус ответа = 400 и фото не добавлено
    # Баг, статус 200 и фото питомца заменено на фото некорректного формата (webp)
        assert status == 400
        assert 'pet_photo' not in result


# Тест №9. БАГ. Добавление фото питомцу с некорректным ID.
def test_add_photo_of_pet_incorrect_pet_id(pet_photo='images/Dog5.jpg'):
    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = '1a2s3d4567'
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа = 400 и фото не добавлено
    # Баг, статус 500
    assert status == 400
    assert 'pet_photo' not in result

# Тест №10. БАГ. Обновление данных о питомце при указании некорректных значений.
def test_successful_update_self_pet_info_not_valid_data(name='', animal_type='', age=''):

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 400 и имя питомца не соответствует заданному пустому значению
        # Баг, статус 200
        assert status == 400
        assert result['name'] is not None
    else:
        # если спиcок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")






































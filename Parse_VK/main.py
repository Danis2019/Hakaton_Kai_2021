from urllib.request import urlretrieve
from const import TOKEN
import vk, os, time, math

# Авторизация
token = TOKEN
session = vk.Session(access_token=token) 
vkapi = vk.API(session, v='5.130')

# Из ссылки извлекаем необходимые параметры для запроса
url = input('Введите url альбома: ')
album_id = url.split('/')[-1].split('_')[1]
owner_id = url.split('/')[-1].split('_')[0].replace('album', '')

#Запрос к VK API
photos_count = vkapi.photos.getAlbums(owner_id=owner_id, album_ids=album_id, v='5.130')['items'][0]['size']
time_now = time.time() # Время старта

# Создание каталогов
if not os.path.exists('saved'):
    os.mkdir('saved')
photo_folder = os.getcwd() + '\\saved\\album{0}_{1}'.format(owner_id, album_id)
if not os.path.exists(photo_folder):
    os.mkdir(photo_folder)

# За один запрос нельзя забрать больше 1000 фото
for j in range(math.ceil(photos_count / 1000)): # Считаем сколько раз нужно получать список фото, так как число получится не целое - округляем в большую сторону
	photos = vkapi.photos.get(owner_id=owner_id, album_id=album_id, photo_sizes=1, count=1000, offset=j*1000, v='5.130') # JSON с кучей инфы
    for pht in photos['items']: # Парсим JSON
        pht_url = ""
        for szs in pht['sizes']:
            if szs.get('type') == 'w':
                pht_url = szs.get('url')
                
        file_name = pht_url.split('/')[5][:15] # Извлекаем имя фотки, сгенерированное ВК
        print(file_name)
        
        try:
            urlretrieve(pht_url, photo_folder + "\\" + file_name) # Загружаем и сохраняем фото
        except Exception:
            print('Произошла ошибка, файл пропущен.')
            continue

time_for_dw = time.time() - time_now
print('Затрачено времени: {} сек.'. format(round(time_for_dw,1)))
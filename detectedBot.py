import cv2

from telebot import TeleBot


# Инициализация бота
API_TOKEN = '6567440090:AAGC0oKTz-R9jKOxQUDmevEmvKc7r_RT8m0'
bot = TeleBot(API_TOKEN)

# Путь к классификатору каскадов Хаара для обнаружения лиц



# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне фото, и я найду лица на нём.")


# Обработчик фотографий
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Загружаем фото
    file_id = message.photo[-1].file_id
    print(message.photo[-1])# Берем фото в максимальном разрешении
    file_info = bot.get_file(file_id)
    print(file_info)
    downloaded_file = bot.download_file(file_info.file_path)
    print(downloaded_file)
    # Сохраняем файл временно
    img_path = 'temp_image.jpg'

    with open(img_path, 'wb') as img_file:
        img_file.write(downloaded_file)

    # Обрабатываем изображение через OpenCV
    result_path, num_faces = detect_faces(img_path)

    # Отправляем пользователю результат
    if num_faces > 0:
        with open(result_path, 'rb') as result_img:
            bot.send_photo(message.chat.id, result_img, caption=f"Я нашел {num_faces} лиц(а) на этом изображении.")
    else:
        bot.reply_to(message, "Лиц не найдено на изображении.")

    # Удаляем временные файлы


def detect_faces(image_path):
    # Загружаем классификатор
    face_cascade = cv2.CascadeClassifier("./cascad/haarcascade_frontalface_default.xml")

    # Чтение изображения
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Обнаружение лиц
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=9, minSize=(5, 5))

    # Отмечаем лица на изображении
    img = cv2.imread("./img/newYear.png")
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        img = cv2.resize(img,(w,h))
        image[y:y + h, x:x + w] = img
        # cv2.imshow(f"{x}img",image[y:y+h,x:x+w])


    # Сохраняем результат во временный файл
    result_path = 'result_image.jpg'
    cv2.imwrite(result_path, image)

    return result_path, len(faces)
# Запуск бота
bot.polling()

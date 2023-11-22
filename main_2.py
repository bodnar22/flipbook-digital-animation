import cv2
import numpy as np
from pytube import YouTube
import os
import time
import asyncio
from aiofiles import open
import moviepy
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def video_download():
    yt = YouTube(
        'https://www.youtube.com/watch?v=H4lMtgmXPys',
        use_oauth=True,
        allow_oauth_cache=True
    )
    print(yt.streams)
    yt.streams.get_by_resolution('360p').download()
    print("Видео успешно загружено")

    # Обрезка видео
    start_time = 4  # Начальное время в секундах
    end_time = 30  # Конечное время в секундах
    input_file = 'Bitch Better Have My Money.mp4'
    output_file = 'output_video.mp4'

    ffmpeg_extract_subclip(input_file, start_time, end_time, targetname=output_file)


async def save_frame(frame, frame_count):
    async with open(f'frames_2/frame_{frame_count:04d}.jpg', 'wb') as f:
        await f.write(cv2.imencode('.jpg', frame)[1])


async def make_shots():
    # Открываем видеофайл
    cap = cv2.VideoCapture('output_video.mp4')

    # Создаем папку для кадров
    if not os.path.exists('frames_2'):
        os.makedirs('frames_2')

    # Считаем кадры
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Сохраняем кадр как изображение
        frame_filename = f'frames_2/frame_{frame_count:04d}.jpg'
        cv2.imwrite(frame_filename, frame)

        await save_frame(frame, frame_count)

        frame_count += 1

    # Закрываем видеофайл
    cap.release()

    # Создаем flipbook
    flipbook_folder = 'flipbook_2'
    if not os.path.exists(flipbook_folder):
        os.makedirs(flipbook_folder)

    # Собираем flipbook из изображений
    circle_first = 69
    circle = 69
    for el in range(frame_count):
        frame_filename = f'frames_2/frame_{el:04d}.jpg'
        frame = cv2.imread(frame_filename)

        # Укажите путь к папке с кадрами
        frames_folder = 'frames_2'

        # Укажите шаг (насколько изменить ширину кадров)
        step = 10  # Например, увеличим ширину каждого кадра на 10 пикселей

        # Получаем список файлов с расширением .jpg из папки с кадрами
        frame_files = [f for f in os.listdir(frames_folder) if f.endswith('.jpg')]
        frame_files.sort()  # Сортируем файлы

        total_frames = len(frame_files)  # Общее количество кадров

        # Проходим по каждому кадру и меняем его размер
        for i, frame_file in enumerate(frame_files):
            frame_path = os.path.join(frames_folder, frame_file)
            frame = cv2.imread(frame_path)

            if i == total_frames:
                break  # Если текущий кадр - последний, выходим из цикла

            # Получаем текущие размеры кадра
            height, width = frame.shape[:2]

            # Изменяем ширину кадра
            if i < circle_first:
                new_width = width  # Изменяем ширину в соответствии с шагом
                new_height = height  # Изменяем высоту в соответствии с шагом
                frame = cv2.resize(frame, (new_width, new_height))

                # Сохраняем кадр с новыми размерами
                # output_path = f'output_frames/frame_{i:04d}.jpg'
                # cv2.imwrite(output_path, frame)
                # print(f'Кадр_{i:04d} сохранен')

                # Подставляем кадр в flipbook
                flipbook_filename = f'{flipbook_folder}/flipbook_{i:04d}.jpg'
                cv2.imwrite(flipbook_filename, frame)
                print(f'Кадр_{i:04d} подставлен')
            elif i != circle + circle_first and i % circle == 0 or i % circle <= 68:
                new_width = width + i * step  # Изменяем ширину в соответствии с шагом
                new_height = height + i * step  # Изменяем высоту в соответствии с шагом
                frame = cv2.resize(frame, (new_width, new_height))

                # Сохраняем кадр с новыми размерами
                # output_path = f'output_frames/frame_{i:04d}.jpg'
                # cv2.imwrite(output_path, frame)
                # print(f'Кадр_{i:04d} сохранен')

                # Подставляем кадр в flipbook
                flipbook_filename = f'{flipbook_folder}/flipbook_{i:04d}.jpg'
                cv2.imwrite(flipbook_filename, frame)
                print(f'Кадр_{i:04d} подставлен')
                if i == total_frames:
                    break  # Если текущий кадр - последний, выходим из цикла
            else:
                # new_width = + width + i * step * circle  # Изменяем ширину в соответствии с шагом
                # frame = cv2.resize(frame, (new_width, height))
                circle += circle_first
                step += 10
                if i == total_frames:
                    break

        # # Сохраняем кадр с новыми размерами
        # output_path = f'output_frames/frame_{i:04d}.jpg'
        # cv2.imwrite(output_path, frame)
        # print(f'Кадр_внешний_{i:04d} сохранен')
        #
        # # Подставляем кадр в flipbook
        # flipbook_filename = f'{flipbook_folder}/flipbook_{i:04d}.jpg'
        # cv2.imwrite(flipbook_filename, frame)
        # print(f'Кадр_внешний_{i:04d} подставлен')

    # В конце, убедитесь, что вы освободили все ресурсы
    cv2.destroyAllWindows()


def create_inner():
    # Указываем путь к папке с кадрами
    frames_folder = 'C:\\Users\\Admin\\Desctop\\Flipbook\\flipbook_2'

    # Получаем список файлов с расширением .jpg из папки с кадрами
    frame_files = [f for f in os.listdir(frames_folder) if f.endswith('.jpg')]
    frame_files.sort()  # Сортируем файлы


    # Определяем размер кадров (берем размер первого кадра)
    frame = cv2.imread(os.path.join(frames_folder, frame_files[0]))
    height, width, layers = frame.shape

    # Указываем путь и имя для выходного видеофайла
    output_video_path = 'C:\\Users\\Admin\\Desctop\\Flipbook\\output_inner_video.mp4'

    # Устанавливаем кодек и частоту кадров
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # XVID - это кодек
    fps = 30  # Частота кадров

    # Создаем объект VideoWriter
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Читаем и записываем кадры в выходное видео
    for frame_file in frame_files:
        frame_path = os.path.join(frames_folder, frame_file)
        frame = cv2.imread(frame_path)
        out.write(frame)

    # Отображаем сообщение о завершении
    print(f'Видео сохранено в: {output_video_path}')
    print('Видео  внутреннее сохранено')

    # Освобождаем ресурсы
    out.release()


def combine_videos():
    # Завантажте ваши відео
    # Создаем объект VideoCapture и передаем ему путь к видеофайлу
    # шаблона
    cap1 = cv2.VideoCapture('C:\\Users\\Admin\\Desctop\\Flipbook\\'
                            'Green Screen Flipbook Animation  Flipbook 3d Addon  Blender.mp4')
    # внутрянка
    cap2 = cv2.VideoCapture('C:\\Users\\Admin\\Desctop\\Flipbook\\output_inner_video.mp4')

    # Проверяем, успешно ли открыт видеофайл
    if not cap1.isOpened():
        print("Ошибка при открытии видеофайла")

    # Переконайтеся, що обидва відео мають однакову роздільну здатність
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output_video.avi', fourcc, 30.0, (int(cap1.get(3)), int(cap1.get(4))))
    out = cv2.VideoWriter('output_video.avi', fourcc, 30.0, (int(cap1.get(3)), int(cap1.get(4))))
    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            pass

        # Визначте діапазон зеленого кольору
        lower_green = np.array([35, 43, 46])
        upper_green = np.array([77, 255, 255])

        # Перетворіть зображення в HSV
        hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

        # Створіть маску для зеленого кольору
        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask_inv = cv2.bitwise_not(mask)

        # Видаліть зелений колір з першого відео
        res1 = cv2.bitwise_and(frame1, frame1, mask=mask_inv)

        # Замініть зелену область другим відео
        res2 = cv2.bitwise_and(frame2, frame2, mask=mask)

        # Об'єднайте обидва результати
        final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

        # Запишіть результат у файл
        out.write(final_output)

        cv2.imshow('final_output', final_output)
        if cv2.waitKey(1) == ord('q'):
            break

        print('Видео смонтировано')

    cap1.release()
    cap2.release()
    out.release()
    cv2.destroyAllWindows()


# video_download()

asyncio.run(make_shots())
create_inner()
combine_videos()

import cv2
import numpy as np
from pytube import YouTube
import os
import time
def make_shots():
    # Открываем видеофайл
    cap = cv2.VideoCapture('Skibidi Toilet Minecraft Villager 3.mp4')

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

        frame_count += 1

    # Закрываем видеофайл
    cap.release()

    # Создаем flipbook
    flipbook_folder = 'flipbook_2'
    if not os.path.exists(flipbook_folder):
        os.makedirs(flipbook_folder)

    # Собираем flipbook из изображений
    for i in range(frame_count):
        frame_filename = f'frames_2/frame_{i:04d}.jpg'
        frame = cv2.imread(frame_filename)

        # Меняем размер кадра, если необходимо
        # frame = cv2.resize(frame, (новая_ширина, новая_высота))

        # Укажите путь к папке с кадрами
        frames_folder = 'frames_2'

        # Укажите шаг (насколько изменить ширину кадров)
        step = 10  # Например, увеличим ширину каждого кадра на 2 пикселей

        # Получаем список файлов с расширением .jpg из папки с кадрами
        frame_files = [f for f in os.listdir(frames_folder) if f.endswith('.jpg')]
        frame_files.sort()  # Сортируем файлы

        # Проходим по каждому кадру и меняем его размер
        for i, frame_file in enumerate(frame_files):
            frame_path = os.path.join(frames_folder, frame_file)
            frame = cv2.imread(frame_path)

            # Получаем текущие размеры кадра
            height, width = frame.shape[:2]

            # Изменяем ширину кадра
            circle_first = 69
            circle = 69
            if i < circle_first:
                new_width = width  # Изменяем ширину в соответствии с шагом
                new_height = height  # Изменяем высоту в соответствии с шагом
                frame = cv2.resize(frame, (new_width, new_height))

                # Сохраняем кадр с новыми размерами
                output_path = f'output_frames/frame_{i:04d}.jpg'
                cv2.imwrite(output_path, frame)

                # Подставляем кадр в flipbook
                flipbook_filename = f'{flipbook_folder}/flipbook_{i:04d}.jpg'
                cv2.imwrite(flipbook_filename, frame)
            elif i != circle + circle_first and i % circle == 0 or i % circle <= 68:
                new_width = width + i * step  # Изменяем ширину в соответствии с шагом
                new_height = height + i * step  # Изменяем высоту в соответствии с шагом
                frame = cv2.resize(frame, (new_width, new_height))

                # Сохраняем кадр с новыми размерами
                output_path = f'output_frames/frame_{i:04d}.jpg'
                cv2.imwrite(output_path, frame)

                # Подставляем кадр в flipbook
                flipbook_filename = f'{flipbook_folder}/flipbook_{i:04d}.jpg'
                cv2.imwrite(flipbook_filename, frame)
            else:
                # new_width = + width + i * step * circle  # Изменяем ширину в соответствии с шагом
                # frame = cv2.resize(frame, (new_width, height))
                circle = circle + circle_first
                step += 10

            # Сохраняем кадр с новыми размерами
            # output_path = f'output_frames/frame_{i:04d}.jpg'
            # cv2.imwrite(output_path, frame)

        # Подставляем кадр в flipbook
        flipbook_filename = f'{flipbook_folder}/flipbook_{i:04d}.jpg'
        cv2.imwrite(flipbook_filename, frame)

    # В конце, убедитесь, что вы освободили все ресурсы
    cv2.destroyAllWindows()

make_shots()
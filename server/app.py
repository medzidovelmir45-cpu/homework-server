import flet as ft
import requests

SERVER_URL = "http://127.0.0.1:8000/homework"

def main(page: ft.Page):
    page.title = "ДЗ и Расписание"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 15

    homework_list = ft.Column(spacing=12)

    def load_homework(e=None):
        homework_list.controls.clear()
        try:
            res = requests.get(SERVER_URL, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if not data:
                    homework_list.controls.append(
                        ft.Text("Домашних заданий пока нет 🎉", size=16, color=ft.Colors.GREY_400)
                    )
                for item in data:
                    # Шапка карточки
                    controls = [
                        ft.Row([
                            ft.Text(item.get('subject', 'Урок'), weight=ft.FontWeight.BOLD, size=18, color=ft.Colors.BLUE_300),
                            ft.Container(
                                content=ft.Text(item.get('date_target', ''), size=12, color=ft.Colors.WHITE),
                                bgcolor=ft.Colors.BLUE_900,
                                padding=5,
                                border_radius=5
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.Text(item.get('task', ''), size=15),
                    ]

                    # Проверка ответа / решения / картинки
                    answer = item.get('answer', '').strip()
                    if answer:
                        controls.append(ft.Divider(height=10, color=ft.Colors.GREY_800))
                        
                        # Если это ссылка на картинку
                        is_img = any(answer.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']) or "i.imgur.com" in answer
                        
                        if is_img:
                            answer_element = ft.Image(src=answer, fit=ft.ImageFit.CONTAIN, border_radius=8)
                        elif answer.startswith("http://") or answer.startswith("https://"):
                            answer_element = ft.ElevatedButton(
                                "🔗 Открыть решение / файл",
                                icon=ft.Icons.LINK,
                                on_click=lambda e, url=answer: page.launch_url(url)
                            )
                        else:
                            answer_element = ft.Text(answer, size=14, color=ft.Colors.WHITE, selectable=True)

                        controls.append(
                            ft.Container(
                                padding=10,
                                border_radius=6,
                                bgcolor=ft.Colors.GREEN_900,
                                content=ft.Column([
                                    ft.Text("💡 Ответ / Решение:", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_200, size=13),
                                    answer_element
                                ])
                            )
                        )

                    # Нижняя панель с датой публикации
                    controls.extend([
                        ft.Divider(height=10, color=ft.Colors.GREY_800),
                        ft.Row([
                            ft.Icon(ft.Icons.ACCESS_TIME, size=14, color=ft.Colors.GREY_500),
                            ft.Text(f"Опубликовано: {item.get('created_at', 'Неизвестно')}", size=12, color=ft.Colors.GREY_500)
                        ])
                    ])

                    homework_list.controls.append(
                        ft.Card(
                            elevation=4,
                            content=ft.Container(
                                padding=16,
                                border_radius=10,
                                content=ft.Column(controls)
                            )
                        )
                    )
            else:
                homework_list.controls.append(ft.Text(f"Ошибка сервера: {res.status_code}", color=ft.Colors.RED_400))
        except Exception as err:
            homework_list.controls.append(
                ft.Text(f"Ошибка при загрузке:\n{err}", color=ft.Colors.RED_400)
            )
        page.update()

    page.add(
        ft.Row([
            ft.Text("Расписание и ДЗ", size=22, weight=ft.FontWeight.BOLD),
            ft.IconButton(icon=ft.Icons.REFRESH, on_click=load_homework, tooltip="Обновить")
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(),
        homework_list
    )

    load_homework()

try:
    ft.app(target=main)
except AttributeError:
    ft.run(main)

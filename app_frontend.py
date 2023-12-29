import flet as ft
from app_backend import predict_action_taken
from typeWriterEffectControl import TypeWriterControl

class InputField(ft.UserControl):
    def __init__(self, width, height, hint_text, icon, password=False):
        super().__init__()
        self.body = ft.Container(
            ft.Row([
                ft.TextField(
                    hint_text=hint_text,
                    border=ft.InputBorder.NONE,
                    color='white',
                    height=height,
                    width=width*(4/5),
                    hint_style=ft.TextStyle(
                        color='white'
                    ),
                    bgcolor='transparent',
                    text_style=ft.TextStyle(
                        size=18,
                        weight='w400',

                    ),
                    password=password
                ),
                ft.Icon(
                    icon,
                    color='white',
                )
                
            ],alignment=ft.MainAxisAlignment.SPACE_AROUND),
            border=ft.border.all(1,'#44f4f4f4'),
            border_radius=18,
            bgcolor='transparent',
            alignment=ft.alignment.center,
            width=width,
        )

    def build(self):
        return self.body

def main(page: ft.Page):
    page.padding = 0
    page.window_width = 1300
    page.window_height = 730
    page.title = 'Proactive Server Resource Management'
    page.window_resizable = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = '#363636'
    page.fonts = {
        'Comfortaa-Bold': 'fonts/Comfortaa-Bold.ttf',
        'Comfortaa-Light': 'fonts/Comfortaa-Light.ttf',
        'Comfortaa-Medium': 'fonts/Comfortaa-Medium.ttf',
        'Comfortaa-Regular': 'fonts/Comfortaa-Bold.ttf',
        'Comfortaa-SemiBold': 'fonts/Comfortaa-SemiBold.ttf',
    }

    predicted_action = ft.Text(value='the output will be generated here...',size=22,color='white',width=700,text_align='center',italic=True,font_family='Comfortaa-Medium')
    user_input = ft.TextField(hint_text='short description...',color='white',border_color='white',multiline=True,text_size=22,width=550,text_align='center',border_radius=18)
    twc = TypeWriterControl(value='the output will be generated here...',font_family='Comfortaa-Medium',text_align='center')

    def get_predicted_action(e):
        user_input.error_text = ""
        page.update()
        if not user_input.value:
            user_input.error_text = "missing short description..."
            page.update()
        else:
            predicted_action.visible = False
            page.update()
            twc.text_to_print = predict_action_taken(str(user_input.value))
            twc.font_family = 'Comfortaa-Medium'
            twc.text_align = 'justify'
            twc.update()
            page.update()

    login_content = ft.Column([
        ft.Text(
            "Login",
            font_family='Comfortaa-Bold',
            color='white',
            weight='w700',
            size=26,
            text_align='center'
        ),
        InputField(
            width=300,
            height=50,
            hint_text='username',
            icon=ft.icons.PERSON_ROUNDED
        ),
        InputField(
            width=300,
            height=50,
            hint_text='password',
            icon=ft.icons.PASSWORD_ROUNDED,
            password=True
        ),
        ft.IconButton(
            icon=ft.icons.ADS_CLICK,
            icon_color='white',
            on_click= lambda _: page.go("/homepage")
        )
    ],alignment=ft.MainAxisAlignment.SPACE_AROUND,horizontal_alignment='center')

    login_page_content = ft.Column([
        ft.Stack([
            ft.Image(
                src='background.jpg',
            ),
            ft.Container(
                content=login_content,
                width=400,
                height=400,
                border_radius=18,
                border=ft.border.all(1,'white'),
                bgcolor='#10f4f4f4',
                blur=ft.Blur(10,12,ft.BlurTileMode.MIRROR),
                alignment=ft.alignment.center,
                right=80,
                top=200,
            ),
        ])
    ],horizontal_alignment='center',alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    homepage_body = ft.Column([
        ft.Stack([
            ft.Image(src='green.jpg'),
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        value='Welcome Anurag, to the Admin Panel !',
                        color='white',
                        weight='w700',
                        size=28,
                        text_align='center',
                        font_family='Comfortaa-Bold'
                    ),
                    ft.Divider(color='green'),
                    ft.Row([
                        user_input,
                        ft.IconButton(
                            icon=ft.icons.SUBDIRECTORY_ARROW_LEFT_OUTLINED,
                            icon_color='white',
                            on_click=get_predicted_action
                        ),
                    ],alignment='center'),
                    ft.Divider(color='green'),
                    # ft.Row([predicted_action],alignment='center'),
                    ft.Row([twc],alignment='center'),
                    ft.Divider(color='green'),
                    ft.IconButton(
                        icon=ft.icons.LOGOUT_ROUNDED,
                        icon_color='white',
                        icon_size=32,
                        on_click=lambda _:page.go('/')
                    )
                ],alignment=ft.MainAxisAlignment.SPACE_AROUND,horizontal_alignment='center'),
                width=900,
                height=600,
                border_radius=22,
                border=ft.border.all(1,'white'),
                bgcolor='#10f4f4f4',
                blur=ft.Blur(10,12,ft.BlurTileMode.MIRROR),
                alignment=ft.alignment.center,
                right=200,
                top=60,
                padding=10
            ),
        ]),
    ],horizontal_alignment='center')

    homepage_content = ft.Container(
        content= homepage_body,
        padding=0,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=['#373737','#232323']
        )
    )

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    login_page_content,
                ],
                scroll="auto",
                vertical_alignment="center",
                horizontal_alignment="center",
                padding=0,
            )
        )
        if page.route == "/homepage":
            page.views.append(
                ft.View(
                    "/homepage",
                    [
                        homepage_content
                    ],
                    scroll="auto",
                    vertical_alignment="center",
                    horizontal_alignment="center",
                    padding=0,
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main, assets_dir='assets', view=ft.WEB_BROWSER)
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.image import AsyncImage
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivy.properties import StringProperty
from kivymd.uix.progressbar import MDProgressBar
from pytube import YouTube, Playlist
from os import getcwd
from kivymd.uix.spinner import MDSpinner
from kivy.metrics import dp
import re
from threading import Thread

Window.size = (450, 740)




kv = '''
ScreenManager:
    Main:
    Progress:
    Setting:
    About:

<Main>: 
    name: 'main'
    BoxLayout:
        orientation:'vertical'
        MDToolbar:
            title: 'YTube'
            elevation: 10
            MDIconButton:
                id: right_button
                icon: 'dots-vertical'
                pos_hint: {'center_y': .5}
                on_release: app.menu.open()

        MDBottomNavigation:
            #panel_color: .2, .2, .2, 1
            elevation: 10

            MDBottomNavigationItem:
                name: 'url'
                text: 'url'
                icon: 'youtube'

                MDScreen:
                    url_input: url_input
                    button: button

                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: 10
                        padding: (30, 100)

                        MDTextField:
                            id: url_input
                            hint_text: 'URL'
                            required: True
                            helper_text_mode: "on_error"
                            focus: True
                            on_text_validate: app.start_downloading()
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: 80
                            pos_hint: {'center_x':.5, 'center_y': .5}
                            adaptive_size: True
                            MDRaisedButton:
                                text: 'Choice a local file'
                                on_release: app.file_manager_open()
                                elevation_normal: 8
                                elevation: 10
                        Widget:
                        MDFloatingActionButton:
                            id: button
                            icon: "download"
                            md_bg_color: app.theme_cls.primary_color
                            pos_hint:{'center_x':.9, 'center_y': .5}
                            elevation: 10
                            on_release: app.start_downloading()
                            # on_release: root.manager.current = 'progress'

            MDBottomNavigationItem:
                name: 'instagram'
                text: 'instagram'
                icon: 'instagram'

                MDLabel:
                    text: 'instagram file download'
                    halign: 'center'

            MDBottomNavigationItem:
                name: 'status'
                text: 'whatsapp status'
                icon: 'account'

                MDLabel:
                    text: 'whats app status download'
                    halign: 'center'
<Progress>:
    name: 'progress'
    video_list: video_list
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'Back'
            left_action_items: [["arrow-left", lambda x: app.home()]]
        Carousel:
            id: video_list
        
                    
                  

<Setting>:
    name: 'setting'
    MDBoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: 'Save path'
        Widget:

<About>:
    name: 'about'
    MDBoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: 'About rohit'
                                                                  

'''


class Main(Screen):
    pass
class Progress(Screen):
    pass
class Setting(Screen):
    pass
class About(Screen):
    pass


sm = ScreenManager()
sm.add_widget(Main(name='main'))
sm.add_widget(Progress(name='progress'))
sm.add_widget(Setting(name='setting'))
sm.add_widget(About(name='about'))


video = None
save_path = None

class Ytube(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.colors = 'Red'
        self.theme_cls.primary_palette = "Red"
        self.root = Builder.load_string(kv) 

        menu_items = [
            {"icon": "application-settings",
            "text": "Setting"},

            {"icon": "account",
            'text': "About"},
        ]
        show_position = self.root.get_screen('main').ids.right_button
        self.menu = MDDropdownMenu(caller=show_position, items=menu_items, width_mult=3)
        self.menu.bind(x = self.drop_down_callback)

        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
   
    # ------------------------------------ file manager -------------------------------------
    def file_manager_open(self):
        self.file_manager.show(getcwd())  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        return self.show_message(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True
    # ------------------------------- File manager end ----------------------------------------
    def loader(self):
        scr_loader = MDSpinner(
            size_hint = (None, None ),
            size = (dp(46), dp(46)),
            pos_hint = {'center_x': .5, "center_y": .5},
            active = True,
            color=[
                [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],
                [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1],
                [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],
                [0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],
            ])
        return scr_loader

    def drop_down_callback(self, obj, value):
        print("this is obj", obj, "This is value: ", value)
        # if instance_menu_items.text == 'Setting':
        #     self.menu.dismiss()
        #     self.root.current = 'setting'
        # else:
        #     self.menu.dismiss()
        #     self.root.current = 'about'

    def start_downloading(self):
        user_input = self.root.get_screen('main').ids.url_input.text        
        if user_input != '':
            self.root.current = 'progress'

            is_video = re.search(r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$', user_input)
            is_playlist = re.search(r'(list)\=.', user_input)

            if is_video:
                display = self.root.get_screen('progress').ids.video_list

                global video
                video = YouTube(user_input)

                for num in range(1):
                    main_layout = MDFloatLayout()
                    flip_card = MDCard(size_hint=(.9, .9), pos_hint={'center_x':.5, 'center_y': .5})
                    box_1 = MDBoxLayout(orientation='vertical',)
                    box_2 = MDBoxLayout(orientation='vertical', )
                    box_3 = MDBoxLayout(orientation='vertical', padding=20)

                    img = AsyncImage(source=video.thumbnail_url, size_hint=(.9, .9), pos_hint={'center_x': .5, 'center_y': .5})
                    
                    box_3.add_widget(img)
                    box_3.add_widget(
                        MDLabel(
                            text=video.title, halign='center', font_style='Body2'
                            )
                                )
                    box_2.add_widget(box_3)
                    box_2.add_widget(MDRaisedButton(text='Download', pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(.6, .1), on_release = self.quality_check,))

                    box_1.add_widget(box_2)
                    advertisement_box = MDBoxLayout(orientation='vertical', size_hint=(1, .2))
                    advertisement_box.add_widget(MDLabel(text='Advertisement', halign='center'))
                    advertisement_box.add_widget(MDProgressBar(pos_hint={"center_x": .5, }))
                    box_1.add_widget(advertisement_box)


                    flip_card.add_widget(box_1)
                    
                    main_layout.add_widget(flip_card)
                    display.add_widget(main_layout)



            elif is_playlist:
                display = self.root.get_screen('progress').ids.video_list

                playlist = Playlist(user_input)
                

                for url in playlist.video_urls:
                    vid = YouTube(url)

                    main_layout = MDFloatLayout()
                    flip_card = MDCard(size_hint=(.9, .9), pos_hint={'center_x':.5, 'center_y': .5})
                    box_1 = MDBoxLayout(orientation='vertical',)
                    box_2 = MDBoxLayout(orientation='vertical', )
                    box_3 = MDBoxLayout(orientation='vertical', padding=20)

                    img = AsyncImage(source=vid.thumbnail_url, size_hint=(.9, .9), pos_hint={'center_x': .5, 'center_y': .5})
                    
                    box_3.add_widget(img)
                    box_3.add_widget(
                        MDLabel(
                            text=vid.title, halign='center', font_style='Body2'
                            )
                                )
                    box_2.add_widget(box_3)
                    box_2.add_widget(MDRaisedButton(text='Download', pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(.6, .1), on_release = self.quality_check,))

                    box_1.add_widget(box_2)
                    advertisement_box = MDBoxLayout(orientation='vertical', size_hint=(1, .2))
                    advertisement_box.add_widget(MDLabel(text='Advertisement', halign='center'))
                    advertisement_box.add_widget(MDProgressBar(pos_hint={"center_x": .5, }))
                    box_1.add_widget(advertisement_box)


                    flip_card.add_widget(box_1)
                    
                    main_layout.add_widget(flip_card)
                    display.add_widget(main_layout)
                viewer = Thread(target=video_parse, args=[playlist])

            else:
                self.show_message('Enter a valid URL!')
            
        else:
            self.show_message('Provide URL address!')
    
    def home(self):
        output = self.root.current = 'main'
        return output

    def show_message(self, text):
        snackbar = Snackbar(
                text=f"{text}",
            )
        return snackbar.show()

    def callback_for_bottom_sheet(self, *args):
        self.show_message(args[0])
        global save_path
        if args[0] == 'Audio':
            vid = video.streams.filter(only_audio=True, type='audio').first()
            print("Video started downlaoding -------")
            return vid.download(save_path)
        else:
            vid = video.streams.filter(only_video=True, resolution=str(args[0])).first()
            print("Video started downlaoding -------")
            return vid.download(save_path)

    def quality_check(self, obj):
        bottom_sheet = MDGridBottomSheet()
        data = {
            "Audio": "file",
            "144p": "quality-low",
            "240p": "quality-low",
            "360p": "quality-medium",
            "480p": "quality-medium",
            "720p": "quality-high",
            "1080p": "quality-high",
        }
        for items in data.items():
            bottom_sheet.add_item(
                items[0],
                lambda x, y=items[0]: self.callback_for_bottom_sheet(y),
                icon_src = items[1]
            )
        return bottom_sheet.open()

    def on_start(self):
        #self.theme_cls.theme_style = "Dark"
        pass

    def build(self):
        return self.root

if __name__ == "__main__":
    Ytube().run()
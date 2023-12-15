import os
import requests
import socket
import threading
import time
import webbrowser as wb
import sys
import kivy
from kivy.core.clipboard import Clipboard as cp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.app import MDApp
from kivymd_extensions.akivymd.uix.imageview import AKImageViewer, AKImageViewerItem
from kivy.properties import StringProperty
from kivymd.toast import toast
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd.uix.snackbar import BaseSnackbar
from kivymd.uix.imagelist import SmartTileWithLabel

if kivy.utils.platform == "android":
    from jnius import autoclass
    from kvdroid.tools import change_statusbar_color, navbar_color,immersive_mode
    from plyer.platforms.android import activity


kv = """
#: import get_color_from_hex kivy.utils.get_color_from_hex

#: import webbrowser webbrowser

#: import MDDialog kivymd.uix.dialog.MDDialog

<MyTile@SmartTileWithLabel>
    size_hint_y: None
    height: "150dp"

<SContent>
    orientation: 'vertical'
    size_hint_y: None
    spacing: '20dp'
    height: '40dp'

    MDProgressBar:
        id: progress
        pos_hint: {"center_y": .5}
        type: "indeterminate"

<Loader>
    orientation: 'vertical'
    size_hint_y: None
    spacing: '20dp'
    height: '40dp'
    
    MDSpinner:
        size_hint: None, None
        size: dp(46), dp(46)
        pos_hint: {'center_x': .5, 'center_y': .5}
        active: True

<Do_Rating>
    orientation: 'vertical'
    size_hint_y: None
    height: '60dp'
    #spacing: '20dp'
    
    MDFlatButton:
        id: rd
        text: 'Rate on google play'
        on_release: webbrowser.open('https://play.google.com/store/apps/details?id=com.pubg.imobile')
        
    MDFlatButton:
        id: rdv
        text: 'Rate personally'
        on_release: app.ratep()

<Rate_P>
    orientation: 'vertical'
    size_hint_y: None
    height: '80dp'
    
    AKRating:
        id: rate
        normal_icon: 'star-box-outline'
        active_icon: 'star-box'
        active_color: 1,0,0.4,1
        animation_type: 'grow'
        pos_hint: {'center_x': .5, 'center_y': .5}

    MDTextField:
        id: rating_text
        #multiline: True
        line_color_normal: get_color_from_hex("#000000")
        hint_text_color_focus: get_color_from_hex("#ffffff")
        line_color_focus: get_color_from_hex("#000000")
        #pos_hint: {'center_x': .5, 'center_y': .6}
    

<CustomSnackbar>

    MDIconButton:
        pos_hint: {'center_y': .5}
        icon: root.icon
        opposite_colors: True

    MDLabel:
        id: text_bar
        size_hint_y: None
        height: self.texture_size[1]
        text: root.text
        #font_size: root.font_size
        theme_text_color: 'Custom'
        text_color: get_color_from_hex('ffffff')
        #shorten: True
        #shorten_from: 'right'
        pos_hint: {'center_y': .5}

<Content>:
    orientation: 'vertical'
    size_hint_y: None
    spacing: '20dp'
    height: '40dp'
    
    MDTextField:
        id: f_name
        text: root.fname()
        line_color_normal: get_color_from_hex("#000000")
        hint_text_color_focus: get_color_from_hex("#ffffff")
        line_color_focus: get_color_from_hex("#000000")

MDScreen:

    MDNavigationLayout:

        ScreenManager:
            id: screen_manager

            MDScreen:
                name: "home"

                MDBoxLayout:
                    orientation: 'vertical'

                    MDToolbar:
                        id: toolbar_H
                        title:'HandWriter'
                        pos_hint: {"top": 1}
                        elevation: 10
                        
                        md_bg_color: get_color_from_hex('#4a4fec')
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
                        right_action_items: [['dots-vertical', lambda x: app.callback_m(x)]]

                    MDBoxLayout:
                        id: box
                        padding: "10dp"
                        orientation:'vertical'

                        CardWithText:
                            padding: '10dp'
                            title: 'enter text'
                            size_hint: 1, 1.7
                            radius: 20, 20, 20, 20
                            #ripple_behavior: False
                            style: 'outlined'
                            elevation:5
                            size: "20dp", "10dp"

                            MDTextField:
                                id: namee
                                multiline: True
                                size: root.size
                                line_color_normal: get_color_from_hex("#ffffff")
                                hint_text_color_focus: get_color_from_hex("#ffffff")
                                line_color_focus: get_color_from_hex("#000000")
                                active_line: False
                                font_size: "18sp"
                                size_hint: root.size_hint
                                hint_text: 'Enter text here'
                        MDBoxLayout:
	                    	MDRaisedButton:
	                            text: 'Proceed'
	                            pos_hint: {"center_y": .9}
	                            size_hint: 1, None
	                            md_bg_color: get_color_from_hex('#4a4fec')
	                            tooltip_text: 'Proceed'
	                            on_release: app.opend()
	                        
                        
            MDScreen:
                name: 'images'
                MDToolbar:
                    id: toolbar_img
                    title:'Images'
                    elevation: 10
                    pos_hint: {"top": 1}
                    md_bg_color: get_color_from_hex('#4a4fec')
                    left_action_items: [["arrow-left-circle", lambda x: app.bhome()]]

                BoxLayout:
                    height: dp(40)
                    orientation: "vertical"
                    size_hint: 1, 1
                    padding: dp(3)
                    spacing: dp(3)
                    FloatLayout:
	                    RecycleView:
	                        MDGridLayout:
	                        	id: ls
	                            cols: 2
	                            row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
	                            row_force_default: True
	                            adaptive_height: True
	                            padding: dp(4), dp(4)
	                            spacing: dp(4)
                            
	                BoxLayout:
	                    size_hint_y: None
	                    height: dp(50)
	                    orientation: "vertical"
	                    spacing: dp(4)     

            MDScreen:
                name: "settings"
                MDBoxLayout:
                    MDToolbar:
                        id: toolbar-1
                        title:'Settings'
                        pos_hint: {"top": 1}
                        elevation: 10
                        md_bg_color: get_color_from_hex('#4a4fec')
                        left_action_items: [["arrow-left-circle", lambda x: app.bhome()]]

                ListItemWithSwitch:
                    text: 'Dark Theme'
                    pos_hint: {"center_y": .8}
                    IconLeftWidget:
                        icon: 'theme-light-dark'
                    RightSwitch:
                        on_active: app.on_checkbox_active(*args)
                        

        MDNavigationDrawer:
            id: nav_drawer

            BoxLayout:
                orientation: 'vertical'
                padding: "10dp"
                spacing: "10dp"

                ScrollView:

                    MDList:
                        OneLineIconListItem:
                            text: 'Home'
                            on_press:
                                nav_drawer.set_state("close")
                                screen_manager.current="home"
                            IconLeftWidget:
                                icon: "home"

                        OneLineIconListItem:
                            text: "Settings"
                            on_release:
                                nav_drawer.set_state("close")
                                root.ids.screen_manager.transition.direction = 'left'
                                screen_manager.current = "settings"
                            IconLeftWidget:
                                icon: 'brightness-7'

                        OneLineIconListItem:
                            text: "Share"
                            on_press: app.callback()
                            IconLeftWidget:
                                icon: "share-variant"

                        OneLineIconListItem:
                            text: 'Downloads'
                            on_release:
                                root.ids.screen_manager.transition.direction = 'left'
                                nav_drawer.set_state('close')
                                app.swift()
                            IconLeftWidget:
                                icon: 'download'

                        OneLineIconListItem:
                            text: "Rate Us"
                            on_release: app.ratings()
                            IconLeftWidget:
                                icon: 'star-circle'

                        OneLineIconListItem:
                            text: "Exit"
                            on_press: app.exit()
                            IconLeftWidget:
                                icon: 'logout'       

        
"""

class ListItemWithCheckbox(OneLineAvatarIconListItem):
    pass

class CardWithText(MDCard, RoundedRectangularElevationBehavior):
    pass

class RightCheckBox(IRightBodyTouch, MDCheckbox):
    pass

class ListItemWithSwitch(OneLineAvatarIconListItem):
    pass

class RightSwitch(IRightBodyTouch, MDSwitch):
    pass

class Content(BoxLayout):
    def fname(self):
        self.ids.f_name.text = ''
        timestr = time.strftime("%Y%m%d%H%M%S")
        text = f'IMG_{timestr}'
        return text

class SContent(BoxLayout):
    pass

class Loader(BoxLayout):
    pass

class CustomSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    md_bg_color = get_color_from_hex('#4a4fec')

class Do_Rating(BoxLayout):
    pass

class Rate_P(BoxLayout):
    pass

class HandWriter(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.Android_back)
        Window.softinput_mode = 'below_target'
        self.menu = None
        self.viewer = None

    def on_start(self):
        self.check_internet()

    def check_internet(self):
        host = '8.8.8.8'
        port = 53
        timeout = 3
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        except socket.error as ex:
            self.show_network_error_dialog()

    def show_network_error_dialog(self):
        dialog = MDDialog(
            title='Network Error',
            text='No Internet Connection',
            auto_dismiss=False,
            buttons=[
                MDRaisedButton(
                    text='RESTART',
                    on_release=self.restart_app,
                    md_bg_color=get_color_from_hex('#4a4fec')
                )
            ]
        )
        dialog.open()

    def restart_app(self, instance):
        os.execv(sys.executable, ['python'] + sys.argv)

    def Android_back(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            self.root.ids.screen_manager.transition.direction = 'right'
            self.root.ids.screen_manager.current = 'home'
        return True

    def build(self):
        self.screen = Builder.load_string(kv)
        items = ['Open file', 'Open PDF', 'About Me']
        menu_items = [
            {
                "text": f'{i}',
                "on_release": lambda x=f'{i}': self.start_action(x)
            } for i in items
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4
        )
        self.menu.bind(on_release=self.callback_m)
        return self.screen

    def start_action(self, text_item):
        self.menu.dismiss()
        if text_item == 'About Me':
            wb.open('https://chakradhar-63e72.web.app/')

    def callback_m(self, button):
        self.menu.caller = button
        self.menu.open()

    def bhome(self):
        self.root.ids.screen_manager.transition.direction = 'right'
        self.root.ids.screen_manager.current = 'home'
        
    def cliptext(self):
        self.root.ids.namee.text = cp.paste()

    def opend(self):
        txt = self.root.ids.namee.text
        if len(txt) == 0:
            self.dialog = MDDialog(
                title='Oops',
                text="You haven't enterd anything",
                #radius=[20, 20, 20, 20],
                buttons=[
                    MDRaisedButton(
                        text='CLOSE',
                        on_release=self.close,
                        md_bg_color=get_color_from_hex('#4a4fec')
                        
                    )
                ]
            )
            self.dialog.open()
        else:
            self.dialog1 = MDDialog(
                title='Enter file name',
                type="custom",
                auto_dismiss=True,
                content_cls=Content(),
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self.maint,
                        md_bg_color=get_color_from_hex('#4a4fec')
                    )
                ]
            )
            self.dialog1.open()

    def maint(self, obj):
        try:
            self.main_t = threading.Thread(target=self.texttohand)
            self.main_t.start()
        except Exception as e:
           return MDDialog(title='Error',text=str(e)).open()
        except:
            return MDDialog(title='Error', text='Try again')        
        
    def texttohand(self):
        self.dialog1.dismiss()
        self.loader = MDDialog(
            title='Loading...',
            type='custom',
            auto_dismiss=False,
            content_cls=Loader()
        )

        txt = self.root.ids.namee.text
        fname = self.dialog1.content_cls.ids.f_name.text

        if len(fname) != 0 and len(txt) !=0:
            self.loader.open()
            file = f'{fname}.png'
            r = requests.get(f"https://pywhatkit.herokuapp.com/handwriting?text={txt}")
            with open(file, "wb") as f:
                f.write(r.content)
                f.close()
            self.snackbar_d = CustomSnackbar(
                text="Done",
                icon="information",
                #snackbar_animation_dir='Left',
                snackbar_x="10dp",
                snackbar_y="10dp"
            )
            self.snackbar_d.size_hint_x = (Window.width - (self.snackbar_d.snackbar_x * 2)) / Window.width
            self.snackbar_d.open()
            file_path = os.path.join(os.getcwd(), file)
            toast(str(f"saved in {file_path}"))
            self.root.ids.screen_manager.current = 'home'
            self.loader.dismiss()
        elif len(fname)==0:
            self.dialog = MDDialog(
                title="Error",
                text="File name cannot be empty",
                #radius=[20, 20, 20, 20],
                buttons=[
                    MDRaisedButton(
                        text='CLOSE',
                        on_release=self.close,
                        md_bg_color=get_color_from_hex('#4a4fec')
                        
                    )
                ]
            )
            self.dialog.open()
        

            
    def build(self):
        self.screen = Builder.load_string(kv)
        items = ['Open file', 'Open PDF','About Me']
        menu_items = [
            {
                "text": f'{i}',
                #"height": dp(100),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f'{i}': self.start_action(x)
             } for i in items
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4
        )
        self.menu.bind(on_release=self.callback_m)
        return self.screen

    def start_action(self, text_item):
        self.menu.dismiss()
        print(text_item)
        if text_item == 'About Me':
            wb.open('https://chakradhar-63e72.web.app/')

    def callback_m(self, button):
        self.menu.caller = button
        self.menu.open()

    def callback(self):

        if kivy.utils.platform == "android":

            string = autoclass('java.lang.String')
            Intent = autoclass('android.content.Intent')
            sendIntent = Intent()
            sendIntent.setAction(Intent.ACTION_SEND)
            sendIntent.setType("text/plain")
            sendIntent.putExtra(Intent.EXTRA_TEXT, string("https://github.com/Drax-dr/handwriter"))
            #sendIntent.setPackage("com.facebook.katana")
            activity.startActivity(sendIntent)

        else:
            pass


    def ratings(self):
        self.rating_d = MDDialog(
            title='Rate Us',
            type='custom',
            content_cls=Do_Rating()
        )
        self.rating_d.open()
        
    def ratep(self):
        self.rating_p = MDDialog(
                title='Rate Us',
                type='custom',
                content_cls=Rate_P(),
                buttons=[
                    MDFlatButton(
                        text='Submit',
                        on_release=self.prate
                    )
                ]
            )
        self.rating_p.open()

    def prate(self, obj):
        print(self.rating_p.content_cls.ids.rate.get_rate())
        self.rating_d.dismiss()
        self.rating_p.dismiss()

    def on_checkbox_active(self, checkbox, value):
        if value:
            if kivy.utils.platform == "android":
                navbar_color('#170e15')
                change_statusbar_color('#170e15', 'black')
            self.theme_cls.theme_style = "Dark"
            self.root.ids.namee.line_color_normal = self.theme_cls.primary_light
            self.root.ids.namee.line_color_focus = self.theme_cls.primary_light

        else:
            if kivy.utils.platform == "android":
                immersive_mode()
                navbar_color('#fcfcfc')
                change_statusbar_color('#fcfcfc', 'white')
            self.root.ids.namee.line_color_normal = get_color_from_hex("#000000")
            self.root.ids.namee.line_color_focus = get_color_from_hex("#000000")
            self.theme_cls.theme_style = "Light"
            
    def wait_d(self):
        self.wt = threading.Thread(target=self.swift)
        self.wt.start()
    def swift(self):
        self.root.ids.ls.clear_widgets()
        self.root.ids.screen_manager.current = 'images'
        dirs = os.listdir('.')

        for files in dirs:
            if files.endswith('.png') or files.endswith('.jpg') or files.endswith('.jpeg'):
                if len(files) == 0:
                    self.root.ids.ls.add_widget(
                        MDLabel(text='No Images Found')
                    )
                else:
                    self.root.ids.ls.add_widget(
                        SmartTileWithLabel(source=files, text=files, on_release=self.showimg)
                    )

    def showimg(self, obj):
        self.viewer = AKImageViewer()
        img_dirs = os.listdir('.')
        for image in img_dirs:
            if image.endswith('.png'):
                self.viewer.add_widget(AKImageViewerItem(source=image))
        self.viewer.open()

    def close(self, obj):
        self.dialog.dismiss()

    def exit(self):
        sys.exit()

if __name__ == '__main__':
    HandWriter().run()

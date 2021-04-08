#!/usr/bin/env python
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
#from plyer import notification
from gardenmat.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

from kivy.core.image import Image
from kivy.uix.image import Image as image
import webbrowser

try:
    from bat import *

except Exception as ex:
    print(ex)
    err = '{}: {})'.format(ex.__class__.__name__, ex)
    print(err)
    #notification.notify(title=err, message=err[50:], timeout=20)
    push_alert(0,0,err)
    


def manag(scr):
    scr.add_widget(Ule(name="ule"))
    scr.add_widget(Alert(name="alert"))
    scr.add_widget(Notif(name="arch"))
    scr.add_widget(Sett(name="set"))


def rysuj(func):
    dane = func
    pltem1=[]
    pltem2=[]
    plwg=[]
    plhum=[]
    #print(dane)
    for x in dane:
        pltem1.append(float(x[2]))
        pltem2.append(float(x[3]))
        plhum.append(float(x[4]))
        plwg.append(float(x[5]))
    #print(plhum)
    #print(plwg)
    ax.patch.set_facecolor('#151515')
    #ax.patch.set_alpha(0.2)
    ax.tick_params(colors='white', which='both', labelsize='xx-large')
    plt.plot(pltem1, label='Temp.Zew')
    plt.plot(pltem2, label='Temp.Wew')
    plt.plot(plhum, label='Wilgotność')
    plt.plot(plwg, label='Waga')
    #ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
    #      fancybox=True, shadow=True, ncol=3)

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
           ncol=4, mode="expand", borderaxespad=0,fontsize='xx-large')

global MenuScreen, Ule, Alert, sm, czas

sm = ScreenManager(transition=NoTransition())

class Err(Label):
    pass
class Maly(image):
    pass
class Menu(FloatLayout):
    texture = Image('image/st.png').texture
    @staticmethod
    def now(name):
        sm.current = name
        

class Ule(Screen):
    
    data, temp, waga, humi = get_inf()
    def up(self):
        global ul_id
        inf=get_inf()
        self.ids.dat.text, self.ids.tem.text, self.ids.wei.text, self.ids.hum.text, = inf
        if inf[0]=="00-00-0000 \n 00:00:00":
            self.ids.cialo.clear_widgets()
            self.ids.cialo.add_widget(image(source="image/Batis_Pszczola.png"))
            self.ids.cialo.add_widget(Button(text="^\nSprawdź swoje połączenie!"))
        else:
            self.ids.cialo.clear_widgets()


class Alert(Screen):   
    
    def up(self):
        def op(instance):
            webbrowser.open('https://notify.run/c/40CiRtPlbZUFnkHg')
    
        dane = get_err()
        self.ids.eror.clear_widgets()
        for i in range(len(dane)):
            tekst = str(dane[i][0]) + '\nKod:' + str(dane[i][2]) + '\n' + str(dane[i][3]) 
            log = Err(text=tekst)
            box = BoxLayout(orientation='horizontal') 
            box.add_widget(Maly())
            box.add_widget(log)
            self.ids.eror.add_widget(box)
        but =Button(text="Więcej", size_hint=(1, None))
        for _ in range(len(dane),5):
            self.ids.eror.add_widget(Err(text=" "))
        but.bind(on_release=op)
        self.ids.eror.add_widget(but)
        self.ids.eror.add_widget(Err(text=" "))
        

class Notif(Screen):
    
    def init(self):
        self.ids.dropdown.dismiss()
    def updt(self,text, time):
        self.ids.dropdown.select(text)        
        self.ids.wykres.clear_widgets()
        ax.clear()        
        rysuj(get_all(time))        
        self.ids.wykres.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def godzina(self,text):
        self.ids.dropdown.select(text)        
        self.ids.wykres.clear_widgets()
        ax.clear()        
        rysuj(get_all_hour())       
        self.ids.wykres.add_widget(FigureCanvasKivyAgg(plt.gcf()))
    
    def dzien(self,text):
        self.ids.dropdown.select(text)        
        self.ids.wykres.clear_widgets()
        ax.clear()        
        rysuj(get_all_day())       
        self.ids.wykres.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def miesiac(self,text):
        self.ids.dropdown.select(text)        
        self.ids.wykres.clear_widgets()
        ax.clear()        
        rysuj(get_all_month())        
        self.ids.wykres.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def rok(self,text):
        self.ids.dropdown.select(text)        
        self.ids.wykres.clear_widgets()
        ax.clear() 
        rysuj(get_all_year())      
        self.ids.wykres.add_widget(FigureCanvasKivyAgg(plt.gcf()))

class Comit(Popup):
    def send(self):
        push_alert(0,1,str(self.ids.alert.text))

class Sett(Screen):
    @staticmethod
    def checkbox_click(value):
        if value is True:
            Window.clearcolor = (40 / 255, 40 / 255, 40 / 255, 1)
        else:
            Window.clearcolor = (255 / 255, 255 / 255, 235 / 255, 1)
    stts="Nieaktywne"


try:
    #ule = [[x] for x in get_ule('001')]
    fig = plt.figure()
    fig.patch.set_facecolor('#202020')
    #fig.patch.set_alpha(0.3)
    ax = fig.add_subplot(111)
    rysuj(get_all(100))
except Exception as ex:
    err = '{}: {})'.format(ex.__class__.__name__, ex)
    print(err)
    #notification.notify(title=err, message=err[50:], timeout=20)

class Wykres(FigureCanvasKivyAgg):
    def __init__(self, **kwargs):
        super(Wykres, self).__init__(plt.gcf(), **kwargs)



class TestApp(App):
    Window.clearcolor = (40 / 255, 40 / 255, 40 / 255, 1)

    def build(self):
        manag(sm)
        return sm

#if __name__ == '__main__':
    #TestApp().run()
# buildozer android debug deploy run

try:
    if __name__ == '__main__':
        TestApp().run()
        
        
      
except Exception as ex:
    print(ex)
    err = '{}: {})'.format(ex.__class__.__name__, ex)
    print(err)
    push_alert(0,0,err)
    #notification.notify(title=err, message=err[50:], timeout=20)
    #notification.notify(title='Prosimy o wysłanie maila z błędem', message='Dziękujemy za współpracę', timeout=20)
    # email.send(recipient='zuzgom@gmail.com', subject ='Error', text=ex, create_chooser=True)
   
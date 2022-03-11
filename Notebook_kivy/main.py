from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.network.urlrequest import UrlRequest
import calendar
import datetime
import json


class MainApp(App):

    def __init__(self):
        super().__init__()

        self.main = BoxLayout(orientation='vertical')
        self.note = GridLayout(rows=1)
        self.board = GridLayout(cols=2, row_force_default=True, row_default_height=40, padding=10)
        self.head = BoxLayout(size_hint=(1, .2))
        self.Main_Calendar = GridLayout(rows=3, row_force_default=True, row_default_height=40)
        self.grid = GridLayout(cols=2, row_force_default=True, row_default_height=100, padding=10, spacing=(10, 10))

        self.now = datetime.datetime.now()
        self.year = self.now.year
        self.month = self.now.month
        self.day = self.now.day
        self.data = str(self.year)+str(self.month)+str(self.day)
        self.week = GridLayout(cols=7)
        for i in range(7):
            self.week.add_widget(Label(text=str(calendar.day_abbr[i])))

        self.calendar = GridLayout(cols=7, rows=7, row_force_default=True, row_default_height=50)
        self.fill_calendar()
        self.create_head()
        self.dele = Button()
        self.header = {'Content-Type': 'application/json'}

    def request(self, instance, *args, **kwargs):
        i = instance.text
        if i == "Записи":
            self.get = UrlRequest('http://fkolonistov.pythonanywhere.com/api/v1/notelist/', on_success=self.fill_board,
                                  on_failure=self.fill_board, req_headers=self.header)
        else:
            data = str(self.year) + str(self.month) + str(i)
            self.get = UrlRequest('http://fkolonistov.pythonanywhere.com/api/v1/note/{}/'.format(str(self.year)+str(self.month)+str(i)),
                                  on_success=self.res,
                                  on_failure=self.add_btn(d=data),
                                  req_headers=self.header)
        if kwargs:
            if kwargs['value'] != 0:
                i = kwargs['value']
                self.get = UrlRequest('http://fkolonistov.pythonanywhere.com/api/v1/notelist/{}/'.format(i), on_success=self.res,
                                  on_failure=self.res, req_headers=self.header)
                self.dele = Button(text="x", font_size=12, pos_hint={'center_x': 1, 'center_y': .5}, size_hint=(.3, 1),
                              ids={'id': i}, on_press=self.delete)
                self.head.add_widget(self.dele)

    def res(self, *args, **kwargs):
        self.note.clear_widgets()
        if self.get.resp_status == 200:
            self.note.clear_widgets()
            labelText = TextInput(text=self.get.result['note'], pos_hint={'center_x': .5, 'center_y': .5},
                                  background_color=(0, 0, 0, 1), foreground_color=(1, 1, 1, 1), padding=(10, 6, 6, 6))
            labelText.bind(text=self.post)
            self.note.add_widget(labelText)

    def add_btn(self, *args, **kwargs):
        self.note.clear_widgets()
        data = str(kwargs['d'])
        grid = GridLayout(rows=3, row_force_default=True, row_default_height=40, col_force_default=True,
                          col_default_width=40, padding=(5, 0, 0, 0))
        add = Button(text="+", on_press=self.add_post, ids={'id': data})
        grid.add_widget(add)
        self.note.add_widget(grid)

    def add_post(self, instance, *args, **kwargs):                   # создается запись
        data = instance.ids['id']
        params = json.dumps({'note': "  ", 'data': data, 'category': 1})
        self.postr = UrlRequest('http://fkolonistov.pythonanywhere.com/api/v1/note/', req_body=params,
                                on_success=self.get_tt,
                                on_failure=self.get_tt,
                                on_error=self.get_tt,
                                req_headers=self.header)

    def get_tt(self, *args, **kwargs):
        d = args[1]['data']
        self.get = UrlRequest('http://fkolonistov.pythonanywhere.com/api/v1/note/{}/'.format(d),
                              on_success=self.res,
                              # on_failure=self.res,
                              req_headers=self.header)

    def add_ln(self, *args):
        params = json.dumps({'note': "  ", 'category': 2})
        self.postr = UrlRequest('http://fkolonistov.pythonanywhere.com/api/v1/notelist/', req_body=params,
                                on_success=self.btn_board_new,
                                on_failure=self.btn_board_new,
                                on_error=self.btn_board_new,
                                req_headers=self.header)

    def btn_board_new(self, *args):
        self.main.remove_widget(self.grid)
        self.main.add_widget(self.note)
        id_post = args[1]['id']
        self.get = UrlRequest('http://fkolonistov.pythonanywhere.com/api/v1/notelist/{}/'.format(id_post),
                                on_success=self.res,
                                # on_failure=self.res,
                                req_headers=self.header)

    def post(self, instance, value):
        post_id = self.get.result['id']
        data = self.get.result['data']
        text = value

        if self.get.result['category'] == 1:
            params = json.dumps({'note': text})
            UrlRequest('http://fkolonistov.pythonanywhere.com/api/v1/note/put/{}/'.format(data), req_body=params,
                       req_headers=self.header)
        else:
            params = json.dumps({'note': text, 'data': self.data})
            UrlRequest('http://fkolonistov.pythonanywhere.com/api/v1/notelist/put/{}/'.format(post_id), req_body=params,
                       req_headers=self.header)

    def fill_calendar(self, *args):
        self.main.remove_widget(self.Main_Calendar)
        self.main.remove_widget(self.note)
        self.Main_Calendar.clear_widgets()
        self.calendar.clear_widgets()
        self.main.remove_widget(self.grid)
        self.main.add_widget(self.Main_Calendar)
        self.head.size_hint = (1, .2)
        month_days = calendar.monthrange(self.year, self.month)[1]
        first_day = calendar.monthrange(self.year, self.month)[0]
        ls = []

        for i in range(7):
            if i != first_day:
                ls.append("")
                i += 1
            else:
                break

        for i in range(month_days):
            ls.append(i + 1)

        for i in ls:
            if i == self.now.day and self.month == self.now.month:
                self.calendar.add_widget(Button(text=str(i), background_color=(1, 1, 1, 1), on_press=self.request))
                self.get = UrlRequest('http://fkolonistov.pythonanywhere.com/api/v1/note/{}/'.format(str(self.year)
                 + str(self.month) + str(self.day)),on_success=self.res, on_failure=self.res)
            else:
                self.calendar.add_widget(Button(text=str(i), background_color=(0, 0, 0, 1), on_press=self.request))

        self.Main_Calendar.add_widget(self.week)
        self.gridhead = GridLayout(cols=3)
        self.gridhead.add_widget(Button(text="<", background_color=(0, 0, 0, 1), on_press=self.next))
        self.gridhead.add_widget(Label(text=str(calendar.month_name[self.month])+" "+str(self.year)))
        self.gridhead.add_widget(Button(text=">", background_color=(0, 0, 0, 1), on_press=self.next))
        self.Main_Calendar.add_widget(self.gridhead)
        self.Main_Calendar.add_widget(self.calendar)

    def fill_board(self, *args):
        self.main.remove_widget(self.Main_Calendar)
        self.main.remove_widget(self.note)
        self.main.remove_widget(self.grid)
        self.head.size_hint = (1, .1)
        if self.get.resp_status == 200:
            for i in self.get.result:
                data = str(i['data'])[:10]
                txt = i['note']
                idd = str(i['id'])
                labelTitle = BoxLayout(orientation="vertical", spacing=-5)
                ll = Button(text=str(data), font_size=12, pos_hint={'center_x': .5, 'center_y': .2}, size_hint=(1, .3),
                            color=(211/255, 211/255, 211/255, 1), ids={'id': idd}, on_press=self.btn_board)
                lll = Button(text=str(txt)[:15], pos_hint={'center_x': .5, 'center_y': .5}, ids={'id': idd},
                             on_press=self.btn_board)

                labelTitle.add_widget(ll)
                labelTitle.add_widget(lll)
                self.grid.add_widget(labelTitle)

        add_note = Button(text="+", on_press=self.add_ln)
        self.grid.add_widget(add_note)
        self.main.add_widget(self.grid)

    def delete(self, ins):
        delete = UrlRequest('http://fkolonistov.pythonanywhere.com/api/v1/notelist/delete/{}/'.format(ins.ids['id']),
                            on_success=self.board_up)

    def board_up(self, instance, *args, **kwargs):
        self.grid.clear_widgets()
        self.head.remove_widget(self.dele)
        self.get = UrlRequest('http://fkolonistov.pythonanywhere.com/api/v1/notelist/', on_success=self.fill_board,
                             on_failure=self.fill_board, req_headers=self.header)

    def btn_board(self, instance):
        self.main.remove_widget(self.grid)
        self.main.add_widget(self.note)
        self.request(instance, value=instance.ids['id'])

    def create_head(self):
        d = ['Календарь', 'Записи', ]
        for i in d:
            self.head.add_widget(Button(text=i, on_press=self.head_listener))

    def next(self, ins, *args):
        if ins.text == '>':
            if self.month == 12:
                self.month = 1
                self.year = self.year + 1
            else:
                self.month = self.month + 1

        elif ins.text == '<':
            if self.month == 1:
                self.month = 12
                self.year = self.year - 1
            else:
                self.month = self.month - 1

        self.main.remove_widget(self.board)
        self.main.remove_widget(self.grid)
        self.fill_calendar()
        self.main.add_widget(self.note)
        self.note.clear_widgets()

    def head_listener(self, instance):
        i = instance.text
        if i == "Календарь":
            self.year = self.now.year
            self.month = self.now.month
            self.day = self.now.day
            self.main.remove_widget(self.board)
            self.main.remove_widget(self.grid)
            self.fill_calendar()
            self.main.add_widget(self.note)
            self.note.clear_widgets()
            self.head.remove_widget(self.dele)

        elif i == "Записи":
            self.main.remove_widget(self.note)
            self.main.remove_widget(self.Main_Calendar)
            self.grid.clear_widgets()
            self.request(instance)
            self.head.remove_widget(self.dele)

    def build(self):
        self.main.add_widget(self.head)
        self.fill_calendar()
        self.main.add_widget(self.note)
        return self.main


if __name__ == '__main__':
    app = MainApp()
    app.run()

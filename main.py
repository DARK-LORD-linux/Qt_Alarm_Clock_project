import sys
import os
import time
import sqlite3

from datetime import datetime
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtMultimedia, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QTime, QPoint
from PyQt5.QtGui import QPixmap, QFont, QPolygon, QPainter, QBrush, QPen, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QLabel, QApplication

selected_melody_name = 'first.mp3'
selected_clock_name = 'Analog clock'
selected_theme = 'dark_theme'
selected_language = 'English'


# класс окна для выбора мелодии
class MelodySelect(QMainWindow):
    def __init__(self, theme, language):
        super().__init__()
        uic.loadUi(f'{os.getcwd()}/components/{language}/{theme}/music_window.ui', self)
        self.setGeometry(400, 200, 300, 380)
        self.setFixedSize(300, 380)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.but = 'first.mp3'
        self.buttonGroup.buttonClicked.connect(self.select_music)
        self.select_melody.clicked.connect(self.open_main_window)
        self.default_upload()

    def closeEvent(self, event):
        self.player.stop()
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.open_main_window()

    # метод для выставления мелодии по умолчанию
    def default_upload(self):
        self.load_mp3(f'{os.getcwd()}/assets/music/first.mp3')
        self.play.clicked.connect(self.player.play)
        self.stop.clicked.connect(self.player.stop)

    # выбор мелодии
    def select_music(self, button):
        self.but = button.text()
        self.load_mp3(f'{os.getcwd()}/assets/music/{button.text()}')
        self.play.clicked.connect(self.player.play)
        self.stop.clicked.connect(self.player.stop)

    def load_mp3(self, filename):
        media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)

    def open_main_window(self):
        global selected_melody_name
        self.player.stop()
        selected_melody_name = self.but[:]
        self.close()


# класс окна выбора циферлатов
class ClockSelect(QMainWindow):
    def __init__(self, theme, language):
        super().__init__()
        uic.loadUi(f'{os.getcwd()}/components/{language}/{theme}/clock_menu.ui', self)
        self.setGeometry(200, 100, 579, 578)
        self.setFixedSize(579, 578)
        self.pixmap = QPixmap(f'{os.getcwd()}/assets/images/analog_clock_photo.png')
        self.label.setPixmap(self.pixmap)
        self.pixmap = QPixmap(f'{os.getcwd()}/assets/images/Clock_12hour.png')
        self.label_2.setPixmap(self.pixmap)
        self.pixmap = QPixmap(f'{os.getcwd()}/assets/images/Clock_24hour.png')
        self.label_3.setPixmap(self.pixmap)
        self.but = 'Analog clock'
        self.buttonGroup.buttonClicked.connect(self.res_clock)
        self.select_clock_but.clicked.connect(self.open_melody_window)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.open_melody_window()

    def res_clock(self, button):
        self.but = button.text()

    def open_melody_window(self):
        global selected_clock_name, open_window
        selected_clock_name = self.but[:]
        self.close()


# класс окна "О программе"
class AboutProgramm(QMainWindow):
    def __init__(self, theme, language):
        super().__init__()
        uic.loadUi(f'{os.getcwd()}/components/{language}/{theme}/about_programm_window.ui', self)
        self.setGeometry(400, 200, 451, 243)
        self.setFixedSize(451, 243)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.pixmap = QPixmap(f'{os.getcwd()}/assets/images/logo.jpeg')
        self.progect_logo.setPixmap(self.pixmap)
        self.ok_button.clicked.connect(self.close_window)

    def close_window(self):
        self.close()


# класс окна выбора языка
class SelectLanguage(QMainWindow):
    def __init__(self, theme, language):
        super().__init__()
        uic.loadUi(f'{os.getcwd()}/components/{language}/{theme}/language_menu_window.ui', self)
        self.setGeometry(400, 200, 393, 103)
        self.setFixedSize(393, 103)
        self.language_list.setCurrentRow(0)
        self.select_button.clicked.connect(self.select_language)
        
    def select_language(self):
        global selected_language
        selected_language = self.language_list.selectedItems()[0].text()
        self.close()

    def closeEvent(self, event):
        self.window = MainWindow(selected_theme, selected_language)
        self.window.show()
        event.accept()


# класс окна прозвона будильника
class AlarmClock(QMainWindow):
    def __init__(self, info, theme, language):
        super().__init__()
        self.setGeometry(350, 250, 511, 302)
        self.setFixedSize(511, 302)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.info = info
        uic.loadUi(f'{os.getcwd()}/components/{language}/{theme}/alarm_clock.ui', self)
        self.close_window_button.clicked.connect(self.close_window_action)
        self.ring()

        self.mel = QTimer()
        self.mel.timeout.connect(self.player_status)
        self.mel.start(1000)

    # метод для прозвона будильника
    def ring(self):
        path = f'{os.getcwd()}/assets/music/{self.info[1]}'
        media = QtCore.QUrl.fromLocalFile(path)
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        self.player.play()

        gif = QtGui.QMovie(f'{os.getcwd()}/assets/images/alarm.gif')
        self.label.setMovie(gif)
        gif.start()

        self.time.setText(self.info[0][:-3])
        self.message.setPlainText(self.info[-1])

    def player_status(self):
        if self.player.state() == 0:
            self.player.play()

    def close_window_action(self):
        self.close()

    def closeEvent(self, event):
        self.mel.stop()
        self.player.stop()
        event.accept()


# класс выбора тем
class ChangeTheme(QMainWindow):
    def __init__(self, theme, language):
        super().__init__()
        uic.loadUi(f'{os.getcwd()}/components/{language}/{theme}/themes_window.ui', self)
        self.setGeometry(200, 200, 920, 441)
        self.setFixedSize(920, 441)
        self.pixmap = QPixmap(f'{os.getcwd()}/assets/images/light_theme.png')
        self.label.setPixmap(self.pixmap)
        self.pixmap = QPixmap(f'{os.getcwd()}/assets/images/dark_theme.png')
        self.label_2.setPixmap(self.pixmap)
        self.current_theme = selected_theme
        self.buttonGroup.buttonClicked.connect(self.select_theme)
        self.select_button.clicked.connect(self.change_theme)

    def select_theme(self, button):
        self.current_theme = button.text().lower()

    def change_theme(self):
        global selected_theme
        selected_theme = self.current_theme
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.change_theme()

    def closeEvent(self, event):
        self.window = MainWindow(selected_theme, selected_language)
        self.window.show()
        event.accept()


# класс окна добавления/изменения будильника
class CreateChangeAlarm(QMainWindow):
    def __init__(self, theme, language, result=False, time=False):
        super().__init__()
        self.theme = theme
        self.result = result
        self.time = time
        self.language = language
        uic.loadUi(f'{os.getcwd()}/components/{language}/{theme}/change_alarm_window.ui', self)
        self.setGeometry(400, 150, 383, 463)
        self.setFixedSize(383, 463)
        self.con = sqlite3.connect(f"{os.getcwd()}/assets/alarms_base/events_list.db")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.change_melody_button.clicked.connect(self.show_melody_select_menu)
        self.apply_button.clicked.connect(self.apply_action)

        self.melody_name_line.setText(selected_melody_name)
        self.alarm_time.setDateTime(datetime.now())

        # таймер для проверки статуса мелодии
        self.music_clock_name_timer = QTimer()
        self.music_clock_name_timer.timeout.connect(self.mel_name)
        self.music_clock_name_timer.start(1)

        if self.result:
            self.descriptions.setPlainText(str(self.result[0][2]))
            self.alarm_time.setDateTime(datetime.strptime(self.result[0][0], '%Y-%m-%d %H:%M:%S'))

    # метод для показывания окна выбора мелодии
    def show_melody_select_menu(self):
        self.window = MelodySelect(self.theme, self.language)
        self.window.show()

    # метод для изменения текущей мелодии в поле
    def mel_name(self):
        self.melody_name_line.setText(selected_melody_name)

    # метод вызова нужного метода изменения/добавления будильника
    def apply_action(self):
        global alarms_changed
        if self.result:
            self.upload_changes()
        else:
            self.add_alarm()
        self.music_clock_name_timer.stop()
        self.close()

    # метод для загрузки изменений будильников в базу данных
    def upload_changes(self):
        cur = self.con.cursor()
        if self.result:
            cur.execute(f"""UPDATE event SET time_and_date=
                        '{self.alarm_time.dateTime().toString('yyyy-MM-dd hh:mm:00')}', 
                        melody='{self.melody_name_line.text()}',
                        notes='{self.descriptions.toPlainText()}'
                        WHERE time_and_date = '{self.result[0][0]}'""")
        self.con.commit()

    # метод для добавления будильника
    def add_alarm(self):
        cur = self.con.cursor()
        time = self.alarm_time.dateTime().toString('yyyy-MM-dd hh:mm:00')
        includes = cur.execute(f"""select time_and_date from event 
                               where time_and_date = '{time}'""").fetchall()
        if len(includes) == 0:
            cur.execute(f"""INSERT INTO event(time_and_date, melody, notes) VALUES('{time}',
                        '{selected_melody_name}', '{self.descriptions.toPlainText()}')""")
            self.con.commit()


# класс основного окна
class MainWindow(QMainWindow):
    def __init__(self, theme, language):
        super().__init__()
        self.theme = theme
        self.language = language
        uic.loadUi(f'{os.getcwd()}/components/{language}/{theme}/main_design.ui', self)
        self.setGeometry(200, 100, 940, 580)
        self.setFixedSize(935, 529)
        self.con = sqlite3.connect(f"{os.getcwd()}/assets/alarms_base/events_list.db")

        self.action_Language.triggered.connect(self.select_language)

        self.action_About_programm.triggered.connect(self.about_programm)
        self.action_About_programm.setShortcut(Qt.Key_F1)

        self.action_Themes.triggered.connect(self.change_theme)

        self.actionQuit.triggered.connect(self.quit)
        self.actionQuit.setShortcut(QKeySequence('Ctrl+Q'))

        self.add_alarm_button.clicked.connect(self.add_alarm)
        self.change_clock_button.clicked.connect(self.show_select_clock)
        self.delete_alarm_button.clicked.connect(self.delete_alarm)
        self.alarms_list_table.itemDoubleClicked.connect(self.alarm_change)

        self.paint = False
        self.clock = False
        self.themes_work = False
        self.language_work = False
        self.result = False
        self.painted_clock_name = ''
        self.draw_a_clock()
        self.upload_alarms()

        # таймер для проверки статуса часов и изменений базы данных
        self.painted_clock = QTimer()
        self.painted_clock.timeout.connect(self.clock_status)
        self.painted_clock.start(500)

        # таймер для проверки времени будильников
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_time)
        self.check_timer.start(1000)

    # метод для прозвона будильника
    def check_time(self):
        cur = self.con.cursor()
        result = cur.execute(f"""SELECT * FROM event WHERE time_and_date =
                             '{str(datetime.now()).split('.')[0]}'""").fetchall()
        if len(result) != 0:
            self.window = AlarmClock(result[0], selected_theme, selected_language)
            self.window.show()
            # удаляем будильник, которые прозвенел, из базы данных
            cur.execute(f"DELETE FROM event WHERE time_and_date = '{result[0][0]}'")
            self.con.commit()
            self.upload_alarms()

    # метод, реализовывающий изменение данных будильников
    def alarm_change(self, elem):
        global selected_melody_name
        self.alarms_list_table.selectRow(elem.row())
        self.upload_alarms()
        rows = [i.row() for i in self.alarms_list_table.selectedItems()]
        ids = [self.alarms_list_table.item(i, 0).text() for i in rows][0]
        cur = self.con.cursor()
        self.result = cur.execute(f"""SELECT * FROM event 
                                  WHERE time_and_date = '{ids}'""").fetchall()
        time = datetime.strptime(self.result[0][0], '%Y-%m-%d %H:%M:%S')
        self.window = CreateChangeAlarm(self.theme, self.language, self.result, time)
        self.window.show()
        selected_melody_name = self.result[0][1][:]

    # метод для вызова окна добавления будильника
    def add_alarm(self):
        self.window = CreateChangeAlarm(self.theme, self.language)
        self.window.show()

    # метод для загрузки будильников из базы данных в таблицу
    def upload_alarms(self):
        cur = self.con.cursor()
        result = cur.execute(f"""SELECT * FROM event
                             ORDER BY time_and_date""").fetchall()
        # Заполнили размеры таблицы
        self.alarms_list_table.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            return
        self.alarms_list_table.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.alarms_list_table.setItem(i, j, QTableWidgetItem(str(val)))
        header = self.alarms_list_table.horizontalHeader()
        title = ['time_and_date', 'melody', 'notes']
        self.alarms_list_table.setHorizontalHeaderLabels(title)
        self.result = []
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

    # метод для удаления будильника
    def delete_alarm(self):
        # Получаем список элементов без повторов и их id
        rows = list(set([i.row() for i in self.alarms_list_table.selectedItems()]))
        ids = [self.alarms_list_table.item(i, 0).text() for i in rows]
        # Спрашиваем у пользователя подтверждение на удаление элементов
        if self.language == 'English':
            valid = QMessageBox.question(
                self, '', "Do you really want to delete alarms with time(s): " + ", ".join(ids),
                QMessageBox.Yes, QMessageBox.No)
        elif self.language == 'Russian':
            valid = QMessageBox.question(
                self, '', "Вы действительно хотите удалить будильники со времен(ем/ами): " + ", ".join(ids),
                QMessageBox.Yes, QMessageBox.No)
        # Если пользователь ответил утвердительно, удаляем элементы.
        # Не забываем зафиксировать изменения
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute("DELETE FROM event WHERE time_and_date IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)
            self.con.commit()
        self.upload_alarms()

    def clock_status(self):
        self.upload_alarms()
        self.draw_a_clock()

    # метод для показывания окна выбора часов
    def show_select_clock(self):
        self.window = ClockSelect(self.theme, self.language)
        self.window.show()

    # метод для отрисовки окна "О программе"
    def about_programm(self):
        self.window = AboutProgramm(self.theme, self.language)
        self.window.show()

    def select_language(self):
        self.window = SelectLanguage(self.theme, self.language)
        self.window.show()
        self.language_work = True
        self.close()

    # класс для отрисовки окна выбора тем
    def change_theme(self):
        self.window = ChangeTheme(self.theme, self.language)
        self.window.show()
        self.themes_work = True
        self.close()

    def remove_clock(self):
        self.paint = False
        self.clock.setParent(None)
        self.timer.stop()

    def quit(self):
        self.close()
        
    # обрабатываем событие закрытия
    def closeEvent(self, event):
        if not self.themes_work and not self.language_work:
            if self.language == 'English':
                valid = QMessageBox.question(
                    self, '', "Do you really want to quit?",
                    QMessageBox.Yes, QMessageBox.No)
            elif self.language == 'Russian':
                valid = QMessageBox.question(
                    self, '', "Вы действительно хотите выйти?",
                    QMessageBox.Yes, QMessageBox.No)
            # Если пользователь ответил утвердительно - закрываем программу
            if valid == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    # метод для выозва отрисовки часов
    def draw_a_clock(self):
        if self.clock:
            self.remove_clock()
        if selected_clock_name != self.painted_clock_name:
            if selected_clock_name == 'Analog clock':
                self.paint = True
                self.analog_clock()
            elif selected_clock_name == '12 hour clock':
                self.hours12_clock()
            else:
                self.hours24_clock()
            painted_clock_name = selected_clock_name[:]

    # метод для отрисовки цифрового циферблата, с форматов времени 12 часов
    def hours12_clock(self):
        fnt = QFont('Jet Brains Mono', 40, QFont.Bold)
 
        self.clock = QLabel(self)
        self.clock.setFont(fnt)
        self.clock.move(15, 250)
        self.clock.resize(340, 145)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime_12hour)
        self.timer.start(1000)

        self.showTime_12hour()
 
    def showTime_12hour(self):
        currentTime = QTime.currentTime()
        displayTxt1 = currentTime.toString('hh:mm:ssap') 
        self.clock.setText(displayTxt1)
        self.clock.show()

    # метод для создания цифрового циферблата, с форматом времени 24 часа
    def hours24_clock(self):
        fnt = QFont('Jet Brains Mono', 45, QFont.Bold)
 
        self.clock = QLabel(self)
        self.clock.setFont(fnt)
        self.clock.move(25, 250)
        self.clock.resize(320, 145)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime_24hour)
        self.timer.start(1000)  # обновлется каждую секунду
 
        self.showTime_24hour()
 
    def showTime_24hour(self):
        currentTime = QTime.currentTime()
        displayTxt1 = currentTime.toString('hh:mm:ss')
        self.clock.setText(displayTxt1)
        self.clock.show()

    # метод для рисования аналоговых часов
    def analog_clock(self):
        self.timer = QTimer(self) 
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

        # создание часовой стрелки
        self.hPointer = QtGui.QPolygon([QPoint(6, 7), 
                                        QPoint(-6, 7), 
                                        QPoint(0, -50)]) 
        
        # создание минутной стрелки
        self.mPointer = QPolygon([QPoint(6, 7), 
                                  QPoint(-6, 7), 
                                  QPoint(0, -70)]) 
  
        # создание секундной стрелки
        self.sPointer = QPolygon([QPoint(1, 1),
                                  QPoint(-1, 1),
                                  QPoint(0, -90)])
        # цвет для минутной и часовой стрелки
        self.bColor = Qt.yellow 
  
        # цвет для секундной стрелки
        self.sColor = Qt.red
  
    # метод для события рисования
    def paintEvent(self, event):
        if self.paint:
            tik = QTime.currentTime() 
 
            # создаём объект рисования
            painter = QPainter(self)

            # метод для рисования стрелок
            # аргументы: значение цета и какие стрелки следует менять
            def drawPointer(color, rotation, pointer): 
                painter.setBrush(QBrush(color))
                painter.save() 
                painter.rotate(rotation) 
                painter.drawConvexPolygon(pointer)
                painter.restore()

            # сглаживание отрисовки
            painter.setRenderHint(QPainter.Antialiasing) 

            # перемещаем часы
            painter.translate(self.width() / 5, self.height() / 1.7)

            # изменяем размер часов под окно
            painter.setPen(QtCore.Qt.NoPen) 

            # рисуем стрелки
            drawPointer(self.bColor, (30 * (tik.hour() + tik.minute() / 60)), self.hPointer) 
            drawPointer(self.bColor, (6 * (tik.minute() + tik.second() / 60)), self.mPointer) 
            drawPointer(self.sColor, (6 * tik.second()), self.sPointer) 
      
            # рисуем фон
            painter.setPen(QPen(self.bColor))  
            for i in range(0, 60): 
                # рисуем стрелки на фоне
                if (i % 5) == 0: 
                    painter.drawLine(87, 0, 97, 0)  
                # поворачиваем
                painter.rotate(6)
            painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow(selected_theme, selected_language)
    ex.show()
    sys.exit(app.exec_())

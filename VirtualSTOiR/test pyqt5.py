import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Создаем кнопку
        self.button = QPushButton('Нажми меня', self)
        self.button.clicked.connect(self.on_button_clicked)

        # Создаем вертикальный layout и добавляем кнопку
        layout = QVBoxLayout()
        layout.addWidget(self.button)

        # Устанавливаем layout для основного окна
        self.setLayout(layout)

        # Настройки окна
        self.setWindowTitle('PyQt5 Пример')
        self.setGeometry(300, 300, 300, 200)

    def on_button_clicked(self):
        # Показываем сообщение при нажатии кнопки
        QMessageBox.information(self, 'Сообщение', 'Вы нажали кнопку!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
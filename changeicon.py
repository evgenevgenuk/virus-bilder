import sys
import os
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QMessageBox, QComboBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import shutil


class IconChanger(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Icon Changer")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #2e2e2e; color: white; font-family: Arial, sans-serif;")

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label_file = QLabel("Виберіть файл для зміни іконки:")
        layout.addWidget(self.label_file)

        self.btn_file = QPushButton("Завантажити файл")
        self.btn_file.clicked.connect(self.load_file)
        layout.addWidget(self.btn_file)

        self.label_icon = QLabel("Виберіть іконку:")
        layout.addWidget(self.label_icon)

        self.icon_combo = QComboBox(self)
        self.icon_combo.addItem("notepad.ico")
        self.icon_combo.addItem("txt.ico")
        self.icon_combo.addItem("exe.ico")
        self.icon_combo.addItem("img.ico")
        layout.addWidget(self.icon_combo)

        self.btn_change_icon = QPushButton("Змінити іконку")
        self.btn_change_icon.clicked.connect(self.change_icon)
        layout.addWidget(self.btn_change_icon)

        self.setLayout(layout)

        self.file_path = ""
        self.icon_path = ""

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Виберіть файл", "", "All Files (*)")
        if file_path:
            self.file_path = file_path
            self.label_file.setText(f"Файл: {os.path.basename(self.file_path)}")

    def change_icon(self):
        if not self.file_path:
            QMessageBox.warning(self, "Помилка", "Виберіть файл для зміни іконки!")
            return

        icon_name = self.icon_combo.currentText()

        # Завантажуємо іконку з репозиторію GitHub
        icon_url = f"https://raw.githubusercontent.com/evgenevgenuk/virus-bilder/main/icons/{icon_name}"
        icon_path = os.path.join(os.path.expanduser("~"), "Desktop", icon_name)

        try:
            # Завантажуємо іконку на комп'ютер
            response = requests.get(icon_url)
            with open(icon_path, "wb") as icon_file:
                icon_file.write(response.content)

            # Зміна іконки файлу
            self.apply_icon(icon_path)

            QMessageBox.information(self, "Успіх", f"Іконка успішно змінена для: {self.file_path}")

        except Exception as e:
            QMessageBox.warning(self, "Помилка", f"Не вдалося змінити іконку: {str(e)}")

    def apply_icon(self, icon_path):
        # Для зміни іконки файлу ми можемо використати сторонні інструменти, наприклад, pyinstaller
        # В даному випадку ми просто копіюємо іконку до файлу, як показано у прикладі нижче
        destination = self.file_path + ".ico"  # Назва файлу з новою іконкою

        try:
            shutil.copy(icon_path, destination)
        except Exception as e:
            QMessageBox.warning(self, "Помилка", f"Не вдалося застосувати іконку: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    changer = IconChanger()
    changer.show()
    sys.exit(app.exec())

import sys
import os
import shutil
import subprocess
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QFileDialog

class PYBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PY Builder")
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet("background-color: #2e2e2e; color: white; font-family: Arial, sans-serif;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label_video = QLabel("Додайте відео (MP4) або завантажте з GitHub:")
        layout.addWidget(self.label_video)

        self.btn_video = QPushButton("Завантажити відео з комп'ютера")
        self.btn_video.clicked.connect(self.load_video)
        layout.addWidget(self.btn_video)

        self.github_url_input = QLineEdit()
        self.github_url_input.setPlaceholderText("Введіть URL відео з GitHub")
        layout.addWidget(self.github_url_input)

        self.btn_video_github = QPushButton("Завантажити відео з GitHub")
        self.btn_video_github.clicked.connect(self.load_video_from_github)
        layout.addWidget(self.btn_video_github)

        self.label_message = QLabel("Текст помилки при закритті:")
        layout.addWidget(self.label_message)

        self.error_text = QLineEdit()
        layout.addWidget(self.error_text)

        self.btn_create = QPushButton("Створити PY")
        self.btn_create.clicked.connect(self.create_py)
        layout.addWidget(self.btn_create)

        self.setLayout(layout)

        self.video_files = []
        self.project_folder = os.path.join(os.path.expanduser("~"), "Desktop", "project_folder")
        os.makedirs(self.project_folder, exist_ok=True)

    def load_video(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Виберіть MP4 відео", "", "MP4 файли (*.mp4)")
        if files:
            for file in files:
                file_name = os.path.basename(file)
                destination = os.path.join(self.project_folder, file_name)
                if not os.path.exists(destination):
                    shutil.copy(file, destination)
                    self.video_files.append(destination)
            self.label_video.setText(f"Додано {len(self.video_files)} відео")

    def load_video_from_github(self):
        url = self.github_url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Помилка", "Введіть URL відео!")
            return
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                file_name = os.path.basename(url)
                video_path = os.path.join(self.project_folder, file_name)
                with open(video_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                self.video_files.append(video_path)
                self.label_video.setText(f"Відео з GitHub завантажено: {file_name}")
            else:
                QMessageBox.warning(self, "Помилка", "Не вдалося завантажити відео.")
        except Exception as e:
            QMessageBox.warning(self, "Помилка", f"Помилка при завантаженні: {str(e)}")

    def create_py(self):
        if not self.video_files:
            QMessageBox.warning(self, "Помилка", "Додайте хоча б одне відео!")
            return
        error_message = self.error_text.text().strip()
        py_output_path = os.path.join(self.project_folder, "output.py")
        video_files_str = ', '.join([f'"{os.path.basename(v)}"' for v in self.video_files])
        try:
            with open(py_output_path, "w") as py_file:
                py_file.write(f"""
import sys
import os
import subprocess

def play_video():
    video_files = [{video_files_str}]
    if video_files:
        subprocess.run(["start", os.path.join(os.path.dirname(__file__), video_files[0])], shell=True)

def main():
    play_video()
    print(f"Помилка: {error_message}")
    sys.exit(f"Закриття з помилкою: {error_message}")

if __name__ == "__main__":
    main()
""")
            QMessageBox.information(self, "Успіх", f"Python файл створено в папці: {self.project_folder}")
        except Exception as e:
            QMessageBox.warning(self, "Помилка", f"Сталася помилка при створенні py файлу: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    builder = PYBuilder()
    builder.show()
    sys.exit(app.exec())

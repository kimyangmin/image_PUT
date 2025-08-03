import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QLabel, QInputDialog, QMessageBox, QWidget, QVBoxLayout, QPushButton
)
from PyQt5.QtGui import QMovie, QFont, QPixmap
from PyQt5.QtCore import Qt, QRect

class DraggableResizableLabel(QLabel):
    GRIP_SIZE = 16
    def __init__(self):
        super().__init__()
        self.offset = None
        self.resizing = False
        self._pixmap = None
        self._movie = None

    def setImage(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext == ".gif":
            self._movie = QMovie(path)
            self.setMovie(self._movie)
            self._movie.jumpToFrame(0)
            self.resize(self._movie.currentPixmap().size())
            self._movie.start()
        else:
            self._pixmap = QPixmap(path)
            self.setPixmap(self._pixmap)
            self.resize(self._pixmap.size())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            rect = self.rect()
            if QRect(rect.width() - self.GRIP_SIZE, rect.height() - self.GRIP_SIZE,
                     self.GRIP_SIZE, self.GRIP_SIZE).contains(event.pos()):
                self.resizing = True
                self.resize_start_pos = event.globalPos()
                self.resize_start_size = self.size()
            else:
                self.offset = event.globalPos() - self.frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.resizing:
            diff = event.globalPos() - self.resize_start_pos
            new_width = max(40, self.resize_start_size.width() + diff.x())
            new_height = max(40, self.resize_start_size.height() + diff.y())
            self.resize(new_width, new_height)
        elif self.offset is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.offset)
        else:
            rect = self.rect()
            if QRect(rect.width() - self.GRIP_SIZE, rect.height() - self.GRIP_SIZE,
                     self.GRIP_SIZE, self.GRIP_SIZE).contains(event.pos()):
                self.setCursor(Qt.SizeFDiagCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        self.resizing = False
        self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("이미지 팝업툴 실행")
        self.setGeometry(600, 300, 340, 170)
        layout = QVBoxLayout(self)
        title = QLabel("이미지 팝업툴에 오신 것을 환영합니다!", self)
        title.setFont(QFont("맑은 고딕", 14, QFont.Bold))
        desc = QLabel(
            "사용법:\n"
            "- gif 폴더에 원하는 gif, jpg, png, webp 파일을 넣으세요.\n"
            "- 실행 후 원하는 이미지를 골라서 창을 띄울 수 있습니다.\n"
            "- 창을 드래그하여 위치를 옮길 수 있습니다.\n"
            "- 종료하시려면 이미지 클릭 후 ALT+F4를 누르세요.\n",
            self
        )
        desc.setFont(QFont("맑은 고딕", 10))
        desc.setWordWrap(True)
        btn = QPushButton("시작하기", self)
        btn.clicked.connect(self.close)
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addWidget(btn, alignment=Qt.AlignRight)

def main():
    app = QApplication([])

    # 1. gif 디렉토리 경로
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    gif_dir = os.path.join(base_dir, "gif")

    # 2. gif 폴더가 없으면 자동 생성
    if not os.path.exists(gif_dir):
        os.makedirs(gif_dir)
        QMessageBox.information(None, "안내", f"gif 폴더가 생성되었습니다!\n\n{gif_dir}\n여기에 이미지 파일을 넣고 실행해 주세요.")
        if sys.platform.startswith("win"):
            os.startfile(gif_dir)
        sys.exit(0)

    # 3. 환영 인트로 창
    welcome = WelcomeWindow()
    welcome.show()
    app.exec_()

    # 4. 지원하는 모든 확장자 리스트
    exts = [".gif", ".jpg", ".jpeg", ".png", ".webp"]
    img_files = [f for f in os.listdir(gif_dir) if os.path.splitext(f)[1].lower() in exts]
    if not img_files:
        QMessageBox.information(None, "알림", f"gif 폴더에 이미지 파일이 없습니다!\n폴더를 열고 원하는 이미지를 복사해 넣으세요.")
        if sys.platform.startswith("win"):
            os.startfile(gif_dir)
        sys.exit(0)

    # 5. 파일 선택
    selected, ok = QInputDialog.getItem(None, "이미지 선택", "실행할 이미지를 고르세요:", img_files, 0, False)
    if not ok or not selected:
        QMessageBox.information(None, "알림", "실행이 취소되었습니다.")
        sys.exit(0)

    img_path = os.path.join(gif_dir, selected)

    # 6. 메인 이미지 창 생성/실행
    label = DraggableResizableLabel()
    label.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
    label.setAttribute(Qt.WA_TranslucentBackground)
    label.setStyleSheet("background: transparent;")
    label.setImage(img_path)  # 확장자 자동 분기
    label.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        QMessageBox.critical(None, "예기치 않은 오류", str(e))
        sys.exit(1)

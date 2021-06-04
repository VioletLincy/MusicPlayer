import sys
import os
import time
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui_player import Ui_Form


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.initialize()

    def initialize(self):
        self.setWindowTitle("Love")
        self.fileName = ""
        self.cur_song = ''
        self.is_pause = True
        self.playlist = QMediaPlaylist()  # 播放列表
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)  # 列表循环
        self.player = QMediaPlayer(self)
        self.player.setPlaylist(self.playlist)

        # 按键
        self.btn_openfile.clicked.connect(lambda: self.btn_openfile_click())
        self.btn_play.clicked.connect(lambda: self.btn_play_click())

        # 进度条
        self.slider_time.sliderMoved[int].connect(lambda: self.player.setPosition(self.slider_time.value()))

        # 计时器:控制进度条和进度时间
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.player_timer)

    def btn_play_click(self):
        if self.is_pause:
            self.is_pause = False
            self.player.play()
            self.btn_play.setText('stop')
            # for debug
            # print('当前播放歌曲： ' + self.cur_song)
        else:
            self.is_pause = True
            self.player.pause()
            self.btn_play.setText('play')

    def btn_openfile_click(self):
        self.playlist.clear()     # 读取歌曲前，清空playlist
        self.fileName, filetype = QFileDialog.getOpenFileName(self, '选择文件', '', '音频文件 (*.wav)')
        # for debug
        # print('当前歌曲路径：' + self.fileName)
        self.cur_song = os.path.basename(self.fileName)
        self.lab_openfile.setText(self.cur_song)
        # 将音频文件添加到playlist
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.fileName)))

        # 正在播放音乐时，中断播放
        if self.is_pause is False:
            self.player.pause()
            self.btn_play.setText('play')

    # 设置进度条和播放时间
    def player_timer(self):
        self.slider_time.setMinimum(0)
        self.slider_time.setMaximum(self.player.duration())
        self.slider_time.setValue(self.slider_time.value() + 1000)

        self.lab_time.setText(time.strftime('%M:%S', time.localtime(self.player.position() / 1000)))
        self.lab_duration.setText(time.strftime('%M:%S', time.localtime(self.player.duration() / 1000)))

        # 进度条满了之后回零
        if self.player.duration() == self.slider_time.value():
            self.slider_time.setValue(0)


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())

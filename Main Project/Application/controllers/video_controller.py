from ..models.services.video_services import VideoServices
from ..view.video_widget import VideoWidget
from ..models.fsm.video_fsm import VideoFSM
from ..models.fsm.app_fsm import ApplicationFSM


# Controlador principal da aplicação, responsável por delegar as responsabilidades aos
# modulos específicos. Quem usa a aplicação (por exemplo, a GUI) conversa apenas com ApplicationController.
class VideoController:

    # DEFINIR ESTADOS

    def __init__(self):
        self.app_fsm = ApplicationFSM()
        self.video_fsm = VideoFSM()
        self.video = VideoServices()
        self.video_widget = None

    def load_video(self, path):
        self.app_fsm.video_ready()
        self.video.load_video(path)

    def play(self):
        self.video_fsm.playing()
        return

    def pause(self):
        self.video_fsm.paused()
        return

    def next_frame(self):
        if self.app_fsm.is_video_ready():
            self.video.next_frame()
        return

    def previous_frame(self):
        if self.app_fsm.is_video_ready():
            self.video.previous_frame()
        return

    def seek(self, frame):
        if self.app_fsm.is_video_ready():
            self.video.seek(frame)
        return

    def get_frame(self):
        if self.app_fsm.is_video_ready():
            return self.video.get_frame()

    def get_next_frame(self):
        if self.app_fsm.is_video_ready():
            return self.video.get_next_frame()

    def format_time(self, seconds):
        if self.app_fsm.is_video_ready():
            return self.video.format_time(seconds)

    # .........................................
    # Properties

    @property
    def fps(self):
        return self.video.fps

    @property
    def total_frames(self):
        return self.video.total_frames

    @property
    def current_frame(self):
        return self.video.current_frame_value

    @property
    def frame_interval(self):
        return self.video.frame_interval

    @property
    def current_frame_image(self):
        return self.video.current_frame_image

    # ------------------------------------------------------------------------------------------------------------------
    #                               Controle de ações específicas para o VideoWidget
    # ------------------------------------------------------------------------------------------------------------------

    def create_video_widget(self):
        self.video_widget = VideoWidget(self.app_fsm)
        return self.video_widget

    def set_lock_roi(self, state: bool):
        # Define o estado da flag
        if self.video_widget:
            self.video_widget.lock_roi = state

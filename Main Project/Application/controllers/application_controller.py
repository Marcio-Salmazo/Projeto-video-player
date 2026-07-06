from ..services.video_services import VideoServices
from ..services.dataset_services import DatasetServices
from ..services.videowidget_services import VideoWidget
from ..fsm.app_fsm import ApplicationFSM


# Controlador principal da aplicação, responsável por delegar as responsabilidades aos
# modulos específicos. Quem usa a aplicação (por exemplo, a GUI) conversa apenas com ApplicationController.
class ApplicationController:

    def __init__(self):
        self.app_fsm = ApplicationFSM()
        self.video = VideoServices(self.app_fsm)
        self.dataset = DatasetServices(self.app_fsm)
        self.video_widget = None

    # ------------------------------------------------------------------------------------------------------------------
    #                               Controle de ações específicas para o VideoWidget
    # ------------------------------------------------------------------------------------------------------------------

    def create_video_widget(self):
        self.video_widget = VideoWidget()
        return self.video_widget

    def set_lock_roi(self, state: bool):
        # Define o estado da flag
        if self.video_widget:
            self.video_widget.lock_roi = state

    # ------------------------------------------------------------------------------------------------------------------
    #                               Controle de ações relacionadas à base de dados
    # ------------------------------------------------------------------------------------------------------------------

    def create_dataset(self, dataset_name):
        self.dataset.create_dataset(dataset_name)

    def open_dataset(self, path):
        return self.dataset.open_dataset(path)

    def add_class(self, name):
        self.dataset.add_class(name)

    def rename_class(self, old_name, new_name):
        self.dataset.rename_class(old_name, new_name)

    def delete_class(self, class_name):
        self.dataset.delete_class(class_name)

    def save_roi(self, frame, roi, class_name):
        self.dataset.save_roi(frame, roi, class_name)

    # .........................................
    # Comparações de estados

    def is_ready(self):
        return self.dataset.is_ready()

    # .........................................
    # Properties

    @property
    def dataset_path(self):
        return self.dataset.base_path

    # ------------------------------------------------------------------------------------------------------------------
    #                   Controle de ações relacionadas à reprodução e funcionalidades do vídeo
    # ------------------------------------------------------------------------------------------------------------------

    def load_video(self, path):
        self.video.load_video(path)

    def play(self):
        self.video.play()

    def pause(self):
        self.video.pause()

    def next_frame(self):
        self.video.next_frame()

    def previous_frame(self):
        self.video.previous_frame()

    def seek(self, frame):
        self.video.seek(frame)

    def get_frame(self):
        return self.video.get_frame()

    def get_next_frame(self):
        return self.video.get_next_frame()

    def format_time(self, seconds):
        return self.video.format_time(seconds)

    # .........................................
    # Comparações de estados

    def is_playing(self):
        return self.video.is_playing()

    def is_paused(self):
        return self.video.is_paused()

    def is_stopped(self):
        return self.video.is_stopped()

    def is_seeking(self):
        return self.video.is_seeking()

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

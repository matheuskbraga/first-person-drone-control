# drone_controller.py
from djitellopy import Tello # <-- Importação corrigida
import cv2

class TelloController:
    def __init__(self):
        self.tello = Tello()
        # Dicionário de estado das velocidades: Esquerda/Direita, Frente/Trás, Cima/Baixo, Rotação (Yaw)
        self.velocities = {
            'left_right': 0,
            'forward_backward': 0,
            'up_down': 0,
            'yaw': 0
        }

    def connect(self):
        """Conecta ao drone e inicializa o fluxo de vídeo."""
        self.tello.connect()
        print(f"Bateria atual: {self.tello.get_battery()}%")
        self.tello.streamon()

    def set_velocity(self, axis, speed):
        """Atualiza a velocidade de um eixo específico."""
        if axis in self.velocities:
            self.velocities[axis] = speed

    def send_rc_control(self):
        """Envia o estado atual das velocidades para o drone."""
        self.tello.send_rc_control(
            self.velocities['left_right'],
            self.velocities['forward_backward'],
            self.velocities['up_down'],
            self.velocities['yaw']
        )

    def takeoff(self):
        self.tello.takeoff()

    def land(self):
        self.tello.land()

    def get_video_frame(self):
        """Captura o frame atual da câmera do drone."""
        frame_read = self.tello.get_frame_read()
        if frame_read is not None:
            return frame_read.frame
        return None
"""
Script para controlar um drone DJI Tello com o teclado e transmitir o vídeo
para um servidor web local, ideal para FPV com um dispositivo móvel e VR Box.

Autor: [Matheus Braga]
Data: [09/10/2025]

Controles do Teclado:
  - T: Descolar (Takeoff)
  - L: Aterrar (Land)
  - Setas Cima/Baixo: Mover para frente/trás
  - Setas Esquerda/Direita: Mover para os lados
  - W/S: Subir/Descer
  - A/D: Girar no próprio eixo (Yaw)
  - ESC: Sair do programa e aterrar o drone
"""

from djitellopy import Tello
import cv2
import pygame
from pygame.locals import *
import numpy as np
import time
from flask import Flask, Response, render_template_string
import threading

# --- Configurações de Velocidade ---
# Velocidade de movimento do drone (0 a 100)
SPEED = 60

# --- Configurações do Flask (Servidor de Vídeo) ---
app = Flask(__name__)
# Frame de vídeo global que será atualizado pelo loop principal
output_frame = None
lock = threading.Lock()

class TelloController:
    """
    Classe principal para gerir a interface do teclado e o controlo do drone.
    """
    def __init__(self):
        # Inicializa o Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))
        pygame.display.set_caption("Tello Keyboard Control")

        # Inicializa o drone Tello
        self.tello = Tello()

        # Dicionário para controlar o estado das teclas
        self.key_states = {
            "up": False, "down": False, "left": False, "right": False,
            "w": False, "s": False, "a": False, "d": False
        }
        
        self.should_stop = False

    def connect_and_prepare(self):
        """Conecta ao Tello e liga os streams."""
        try:
            self.tello.connect()
            self.tello.streamon()
            print(f"Bateria: {self.tello.get_battery()}%")
            return True
        except Exception as e:
            print(f"Erro ao conectar ao Tello: {e}")
            return False

    def handle_key_event(self, event):
        """Processa eventos de pressionar e soltar teclas."""
        if event.type == KEYDOWN:
            if event.key == K_t: self.tello.takeoff()
            if event.key == K_l: self.tello.land()
            if event.key == K_ESCAPE: self.should_stop = True

            # Atualiza o estado das teclas de movimento
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d]:
                self.update_key_state(event.key, True)

        elif event.type == KEYUP:
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d]:
                self.update_key_state(event.key, False)
    
    def update_key_state(self, key, is_pressed):
        """Atualiza o dicionário de estado das teclas."""
        key_map = {
            K_UP: "up", K_DOWN: "down", K_LEFT: "left", K_RIGHT: "right",
            K_w: "w", K_s: "s", K_a: "a", K_d: "d"
        }
        if key in key_map:
            self.key_states[key_map[key]] = is_pressed

    def send_drone_commands(self):
        """Envia comandos de movimento contínuo para o drone."""
        # [left_right, fwd_bwd, up_down, yaw]
        left_right = (SPEED if self.key_states["right"] else 0) - (SPEED if self.key_states["left"] else 0)
        fwd_bwd = (SPEED if self.key_states["up"] else 0) - (SPEED if self.key_states["down"] else 0)
        up_down = (SPEED if self.key_states["w"] else 0) - (SPEED if self.key_states["s"] else 0)
        yaw = (SPEED if self.key_states["d"] else 0) - (SPEED if self.key_states["a"] else 0)

        self.tello.send_rc_control(left_right, fwd_bwd, up_down, yaw)

    def run(self):
        """Loop principal que gere os eventos, comandos e o stream de vídeo."""
        if not self.connect_and_prepare():
            return

        global output_frame
        frame_read = self.tello.get_frame_read()
        
        while not self.should_stop:
            # Captura eventos do Pygame (teclado)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.should_stop = True
                self.handle_key_event(event)

            # Envia os comandos de movimento
            self.send_drone_commands()

            # Captura e atualiza o frame de vídeo para o servidor
            if frame_read.stopped:
                break
            
            frame = frame_read.frame
            with lock:
                output_frame = frame.copy()

            # Pequena pausa para não sobrecarregar o CPU
            time.sleep(1 / 30)

        # Aterrar e limpar
        print("Aterrando...")
        self.tello.land()
        self.tello.streamoff()
        pygame.quit()

# --- Funções do Servidor Flask ---

def generate_video():
    """Gerador que produz os frames de vídeo para o stream."""
    global output_frame
    while True:
        with lock:
            if output_frame is None:
                continue
            
            # Converte o frame para JPEG
            (flag, encoded_image) = cv2.imencode(".jpg", output_frame)
            if not flag:
                continue
        
        # Produz o frame como uma resposta HTTP
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
              bytearray(encoded_image) + b'\r\n')

@app.route("/")
def index():
    """Página principal que exibe o vídeo."""
    # Um HTML simples para exibir o stream em ecrã inteiro
    return render_template_string(
        """
        <html>
        <head>
            <title>Tello FPV Stream</title>
            <style>
                body, html { margin: 0; padding: 0; overflow: hidden; background-color: #000; }
                img { width: 100%; height: 100%; object-fit: contain; }
            </style>
        </head>
        <body>
            <img src="{{ url_for('video_feed') }}">
        </body>
        </html>
        """
    )

@app.route("/video_feed")
def video_feed():
    """A rota que fornece o stream de vídeo."""
    return Response(generate_video(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

def run_flask_app():
    """Inicia o servidor Flask."""
    # Usar 0.0.0.0 para tornar o servidor acessível na sua rede local
    app.run(host="0.0.0.0", port=5000, threaded=True)

# --- Ponto de Entrada Principal ---

if __name__ == '__main__':
    # Inicia o servidor Flask numa thread separada
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    # Inicia o controlador do drone
    controller = TelloController()
    controller.run()
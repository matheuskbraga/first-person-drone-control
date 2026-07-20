import customtkinter as ctk
from PIL import Image
import cv2

class DroneInterface(ctk.CTk):
    def __init__(self, drone_controller):
        super().__init__()
        
        self.drone = drone_controller
        self.title("Tello Control Center - CustomTkinter")
        self.geometry("800x600")
        
        # Define o tema moderno
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Label que servirá de "tela" para o vídeo
        self.video_label = ctk.CTkLabel(self, text="Aguardando vídeo...")
        self.video_label.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Controle de estado de teclas pressionadas para evitar conflitos de repetição do SO
        self.pressed_keys = set()
        
        # Velocidade padrão de movimentação (0 a 100)
        self.speed = 50 

        self._bind_events()
        
        # Inicia os laços contínuos
        self._update_video_feed()
        self._send_drone_commands()

    def _bind_events(self):
        """Mapeia os eventos de teclado do Tkinter."""
        self.bind("<KeyPress>", self._on_key_press)
        self.bind("<KeyRelease>", self._on_key_release)

    def _on_key_press(self, event):
        """Registra a tecla pressionada e atualiza o estado."""
        key = event.keysym.lower()
        self.pressed_keys.add(key)
        self._calculate_movement()

        # Comandos de disparo único (Takeoff / Land)
        if key == 't':
            self.drone.takeoff()
        elif key == 'l':
            self.drone.land()

    def _on_key_release(self, event):
        """Remove a tecla solta e zera o movimento correspondente."""
        key = event.keysym.lower()
        if key in self.pressed_keys:
            self.pressed_keys.discard(key)
        self._calculate_movement()

    def _calculate_movement(self):
        """
        LÓGICA DE MAPEAMENTO (Personalize aqui)
        Lê o conjunto de teclas pressionadas e define os eixos de velocidade.
        """
        # Cima e Baixo
        if 'w' in self.pressed_keys:
            self.drone.set_velocity('up_down', self.speed)
        elif 's' in self.pressed_keys:
            self.drone.set_velocity('up_down', -self.speed)
        else:
            self.drone.set_velocity('up_down', 0)

        # Frente e Trás (Exemplo com setas direcionais)
        if 'up' in self.pressed_keys:
            self.drone.set_velocity('forward_backward', self.speed)
        elif 'down' in self.pressed_keys:
            self.drone.set_velocity('forward_backward', -self.speed)
        else:
            self.drone.set_velocity('forward_backward', 0)

        # Adicione os mapeamentos para 'left_right' (Esquerda/Direita) 
        # e 'yaw' (Rotação) seguindo a mesma estrutura de if/elif/else acima.

    def _send_drone_commands(self):
        """Loop contínuo que envia os RC Controls para o drone a cada 50ms."""
        self.drone.send_rc_control()
        self.after(50, self._send_drone_commands)

    def _update_video_feed(self):
        """Captura o frame do drone, converte e atualiza a interface a cada 30ms (~33 FPS)."""
        cv2_frame = self.drone.get_video_frame()
        
        if cv2_frame is not None:
            # Converte as cores de BGR (OpenCV) para RGB (Pillow/Tkinter)
            rgb_frame = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB)
            
            # Converte a matriz NumPy em Imagem PIL
            pil_image = Image.fromarray(rgb_frame)
            
            # Cria o objeto CTkImage e redimensiona
            ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(720, 480))
            
            # Atualiza o componente visual
            self.video_label.configure(image=ctk_image, text="")
            
        self.after(30, self._update_video_feed)
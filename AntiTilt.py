from pynput.keyboard import Listener, Key, Controller
import tkinter as tk
import threading

# Dicionário de palavras ofensivas e suas substituições
replacements = {
    "idiota": "Lindo",
    "lixo": "gostoso",
    "podre": "amado",
    "arrombado": "maravilhoso"
}

class Recorder:
    def __init__(self):
        self.buffer = ""  # Armazena o texto digitado
        self.keyboard = Controller()  # Controlador para simular ações do teclado
        self.listener = None  # Listener do teclado

    def on_press(self, key):
        """Chamado quando uma tecla é pressionada."""
        if key == Key.space:  # Avalia a palavra ao pressionar espaço
            self.evaluate_word()
            self.buffer = ""  # Limpa o buffer após avaliação
        elif key == Key.backspace:  # Remove o último caractere do buffer
            self.buffer = self.buffer[:-1]
        else:
            try:
                self.buffer += key.char  # Adiciona o caractere pressionado ao buffer
            except AttributeError:
                pass  # Ignora teclas especiais

    def on_release(self, key):
        """Chamado quando uma tecla é solta."""
        if key == Key.esc:
            # Para o Listener quando a tecla Esc é pressionada
            return False

    def evaluate_word(self):
        """Verifica o buffer para substituir palavras ofensivas."""
        # Transforma o buffer em letras minúsculas para comparação
        word_lower = self.buffer.lower()
        for curse_word, replacement in replacements.items():
            if curse_word in word_lower:
                # Apaga a palavra digitada
                for _ in range(len(self.buffer)):
                    self.keyboard.press(Key.backspace)
                    self.keyboard.release(Key.backspace)
                # Digita a palavra substituta
                self.keyboard.type(replacement)
                break

    def start_listener(self):
        """Inicia o Listener em uma thread separada."""
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def stop_listener(self):
        """Para o Listener."""
        if self.listener:
            self.listener.stop()
            self.listener = None

# Funções para o botão de On/Off
def toggle_listener():
    global listener_running
    if listener_running:
        recorder.stop_listener()
        listener_running = False
        button_on_off.config(text="Ligar")
    else:
        recorder.start_listener()
        listener_running = True
        button_on_off.config(text="Desligar")

# Configuração da interface gráfica
recorder = Recorder()
listener_running = False  # Estado inicial do Listener

# Criando a janela principal
root = tk.Tk()
root.title("Teclado Limpo")
root.geometry("300x200")

# Texto de instrução
label = tk.Label(root, text="Clique no botão para ligar/desligar o filtro", font=("Arial", 12))
label.pack(pady=20)

# Botão de On/Off
button_on_off = tk.Button(root, text="Ligar", font=("Arial", 14), command=toggle_listener, bg="green", fg="white")
button_on_off.pack(pady=10)

# Rodando a janela
root.mainloop()

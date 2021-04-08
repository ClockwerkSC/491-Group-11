import pygame
from touch import MainTouch, PartialTouch
import speech_recognition as sr
import RPi.GPIO as GPIO
import time


class Functions():
    def __init__(self):
        pygame.init()
        self.DISPLAY_W, self.DISPLAY_H = 800, 480
        self.canvas = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W,self.DISPLAY_H))
        self.background = pygame.image.load('real_background.png')
        self.clock = pygame.time.Clock()
        self.running = True
        self.main_running = True
        self.frequency_running = True
        self.person_running = True
        self.audio_running = True
        self.word_running = True
        self.fingers = {}
        
        self.main_flag = False
        self.frequency_flag = False
        self.word_flag = False 
        self.person_flag = False
        self.audio_flag = False

        self.keywords = ['hello', 'stop', 'wait', 'help', 'excuse me', "howdy", "John", "sir", "ma'am", "would you like"]
        self.detected_keywords = []
        
        self.pin = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def check_events(self, touchcontrol = False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.main_running, self.frequency_running, self.word_running, self.person_running, self.audio_running = False, False, False, False, False, False
               

            if touchcontrol != False:
                if event.type == pygame.FINGERDOWN:
                    self.fingers[event.finger_id] = {'x': event.x * self.DISPLAY_W, 'y': event.y * self.DISPLAY_H, 'fresh_pressed': True}
                
                elif event.type == pygame.FINGERMOTION:
                    if event.finger_id in self.fingers:
                        self.fingers[event.finger_id].update({'x': event.x * self.DISPLAY_W, 'y': event.y * self.DISPLAY_H, 'fresh_pressed': False})

                elif event.type == pygame.FINGERUP:
                    if event.finger_id in self.fingers:
                        del self.fingers[event.finger_id]

                for finger in list(self.fingers):
                        touchcontrol.touch_input(self.fingers.get(finger))
                        
                        if touchcontrol.FREQUENCY_BUTTON:
                            print(" FREQUENCY PRESSED")
                            self.frequency_flag = True
                            del self.fingers[finger]

                        if touchcontrol.WORD_BUTTON:
                            print(" WORD PRESSED")
                            self.word_flag = True
                            del self.fingers[finger]

                        if touchcontrol.PERSON_BUTTON:
                            print(" PERSON PRESSED")
                            self.person_flag = True
                            del self.fingers[finger]

                        if touchcontrol.AUDIO_BUTTON:
                            print(" AUDIO PRESSED")
                            self.audio_flag = True
                            del self.fingers[finger]

                        if touchcontrol.EXIT_BUTTON:
                            print(" EXIT PRESSED")
                            self.main_flag = True
                            del self.fingers[finger]
                        

    def reset_fingers(self):
        self.fingers = {}           

    def draw_text(self, display, text, size, x, y, mode):

        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        if mode == "left":
            text_rect.topleft = (x,y)
        elif mode == "center":
            text_rect.center = (x,y)
        display.blit(text_surface, text_rect)

    def main_menu(self):
        self.touch_main = MainTouch()
        while self.main_running:
            self.check_events(self.touch_main)
            self.canvas.blit(self.background, (0,0))
            self.touch_main.touch_draw(self.canvas)
            self.window.blit(self.canvas, (0,0))
            pygame.display.update()
            self.touch_main.reset_touch()
            if self.word_flag or self.frequency_flag or self.person_flag or self.audio_flag:
                self.main_running = False
            
      
    def frequency_analysis_function(self):
        self.touch_frequency = PartialTouch()
        while self.frequency_running:
            self.check_events(self.touch_frequency)
            self.canvas.blit(self.background, (0,0))
            self.draw_text(self.canvas, 'Frequency Analysis WIP', 20, 400, 240, 'center')
            self.touch_frequency.touch_draw(self.canvas)
            self.window.blit(self.canvas, (0,0))
            pygame.display.update()
            self.touch_frequency.reset_touch()
            if self.main_flag:
                self.frequency_running = False            


    def word_vibrate(self):
        for i in range(0, 3):
            GPIO.output(self.pin, GPIO.HIGH)
            print("high")
            time.sleep(.25)
            GPIO.output(self.pin,GPIO.LOW)
            print("low")
            time.sleep(.25)

    def callback(self, recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
        try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
            
            recognized_audio = recognizer.recognize_google(audio)
            print(recognized_audio)
            for keyword in self.keywords:
                if keyword in recognized_audio:
                    print("Key word is " + keyword)
                    self.detected_keywords.append(keyword)
                    self.last_updated_time =  pygame.time.get_ticks()
                    self.word_vibrate()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


    def word_recognition_function(self):
        self.last_updated_time = 0
        self.touch_word = PartialTouch()
        r = sr.Recognizer()
        m = sr.Microphone(device_index=1)
        with m as source:
            r.adjust_for_ambient_noise(source, duration = 0.5) 
        stop_listening = r.listen_in_background(m, self.callback)
        while self.word_running:
        
            self.check_events(self.touch_word)
            pygame.draw.rect(self.canvas, (0,0,0), (0,0, 800, 480))
            #self.canvas.blit(self.background, (0,0))
            if self.detected_keywords:
                for index, keyword in enumerate(self.detected_keywords):
                    self.draw_text(self.canvas, "Detected Keywords:", 25, 400, 150, 'center')
                    self.draw_text(self.canvas, keyword, 20, 400, 200 + index * 25, 'center')
                now = pygame.time.get_ticks()
                if now - self.last_updated_time > 5000:
                    self.detected_keywords.clear()
            else:
                self.draw_text(self.canvas, 'Listening', 20, 400, 240, 'center')
            self.touch_word.touch_draw(self.canvas)
            self.window.blit(self.canvas, (0,0))
            pygame.display.update()
            self.touch_word.reset_touch()
            if self.main_flag:
                stop_listening(wait_for_stop=False)
                self.word_running = False

    def person_detection_function(self):
        self.touch_person = PartialTouch()
        while self.person_running:
            self.check_events(self.touch_person)
            self.canvas.blit(self.background, (0,0))
            self.draw_text(self.canvas, 'Person Detection WIP', 20, 400, 240, 'center')
            self.touch_person.touch_draw(self.canvas)
            self.window.blit(self.canvas, (0,0))
            pygame.display.update()
            self.touch_person.reset_touch()
            if self.main_flag:
                self.person_running = False

    def audio_playback_function(self):
        self.touch_audio = PartialTouch()
        while self.audio_running:
            self.check_events(self.touch_audio)
            self.canvas.blit(self.background, (0,0))
            self.draw_text(self.canvas, 'Audio Playback WIP', 20, 400, 240, 'center')
            self.touch_audio.touch_draw(self.canvas)
            self.window.blit(self.canvas, (0,0))
            pygame.display.update()
            self.touch_audio.reset_touch()
            if self.main_flag:
                self.audio_running = False
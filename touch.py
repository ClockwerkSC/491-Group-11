import pygame

class Touch():
    def __init__(self):
        self.font_name = 'Pokemon Classic.ttf'
        self.WORD_BUTTON, self.FREQUENCY_BUTTON, self.PERSON_BUTTON, self.AUDIO_BUTTON, self.EXIT_BUTTON = False, False, False, False, False


    def reset_touch(self):
        self.WORD_BUTTON, self.FREQUENCY_BUTTON, self.PERSON_BUTTON, self.AUDIO_BUTTON, self.EXIT_BUTTON = False, False, False, False, False

    def draw_text(self, display, text, size, x, y, mode):

        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        if mode == "left":
            text_rect.topleft = (x,y)
        elif mode == "center":
            text_rect.center = (x,y)
        display.blit(text_surface, text_rect)

class MainTouch(Touch):
    def __init__(self):
        Touch.__init__(self)

        #creating frequency analysis button
        self.frequency_analysis_button_x_offset = 50
        self.frequency_analysis_button_y_offset = 50
        self.frequency_analysis_button = pygame.image.load('button background.png')
        self.frequency_analysis_button_rect = self.frequency_analysis_button.get_rect()
        self.frequency_analysis_button_rect.topleft = (self.frequency_analysis_button_x_offset, self.frequency_analysis_button_y_offset)

        #creating word recognition button
        self.word_recognition_button_x_offset = 550
        self.word_recognition_button_y_offset = 50
        self.word_recognition_button = pygame.image.load('button background.png')
        self.word_recognition_button_rect = self.word_recognition_button.get_rect()
        self.word_recognition_button_rect.topleft = (self.word_recognition_button_x_offset, self.word_recognition_button_y_offset)
    
        #creating person detection button
        self.person_detection_button_x_offset = 50
        self.person_detection_button_y_offset = 330
        self.person_detection_button = pygame.image.load('button background.png')
        self.person_detection_button_rect = self.frequency_analysis_button.get_rect()
        self.person_detection_button_rect.topleft = (self.person_detection_button_x_offset, self.person_detection_button_y_offset)

         #creating audio playback button
        self.audio_playback_button_x_offset = 550
        self.audio_playback_button_y_offset = 330
        self.audio_playback_button = pygame.image.load('button background.png')
        self.audio_playback_button_rect = self.word_recognition_button.get_rect()
        self.audio_playback_button_rect.topleft = (self.audio_playback_button_x_offset, self.audio_playback_button_y_offset)

    def touch_draw(self, display):
    
        #display frequency analysis button
        display.blit(self.frequency_analysis_button, self.frequency_analysis_button_rect)
        self.frequency = self.draw_text(display, 'FREQUENCY', 15, self.frequency_analysis_button_rect.centerx, self.frequency_analysis_button_rect.centery - 10, "center")
        self.analysis = self.draw_text(display, 'ANALYSIS', 15, self.frequency_analysis_button_rect.centerx, self.frequency_analysis_button_rect.centery + 10, "center")

        #display word recognition button
        display.blit(self.word_recognition_button, self.word_recognition_button_rect)
        self.word = self.draw_text(display, 'WORD', 15, self.word_recognition_button_rect.centerx, self.word_recognition_button_rect.centery - 10, "center")
        self.recognition = self.draw_text(display, 'RECOGNITION', 15, self.word_recognition_button_rect.centerx, self.word_recognition_button_rect.centery + 10, "center")
    
        #display person detection button
        display.blit(self.person_detection_button, self.person_detection_button_rect)
        self.person = self.draw_text(display, 'PERSON', 15, self.person_detection_button_rect.centerx, self.person_detection_button_rect.centery - 10, "center")
        self.detection = self.draw_text(display, 'DETECTION', 15, self.person_detection_button_rect.centerx, self.person_detection_button_rect.centery + 10, "center")

        #display audio playback button
        display.blit(self.audio_playback_button, self.audio_playback_button_rect)
        self.audio = self.draw_text(display, 'AUDIO', 15, self.audio_playback_button_rect.centerx, self.audio_playback_button_rect.centery - 10, "center")
        self.playback = self.draw_text(display, 'PLAYBACK', 15, self.audio_playback_button_rect.centerx, self.audio_playback_button_rect.centery + 10, "center")

    def touch_input(self, finger):
         
        if (self.frequency_analysis_button_rect.left) <= finger['x'] <= (self.frequency_analysis_button_rect.right):
            if (self.frequency_analysis_button_rect.top) <= finger['y'] <= (self.frequency_analysis_button_rect.bottom): 
                self.FREQUENCY_BUTTON = True

        if (self.word_recognition_button_rect.left) <= finger['x'] <= (self.word_recognition_button_rect.right):
            if (self.word_recognition_button_rect.top) <= finger['y'] <= (self.word_recognition_button_rect.bottom): 
                self.WORD_BUTTON = True

        if (self.person_detection_button_rect.left) <= finger['x'] <= (self.person_detection_button_rect.right):
            if (self.person_detection_button_rect.top) <= finger['y'] <= (self.person_detection_button_rect.bottom): 
                self.PERSON_BUTTON = True

        if (self.audio_playback_button_rect.left) <= finger['x'] <= (self.audio_playback_button_rect.right):
            if (self.audio_playback_button_rect.top) <= finger['y'] <= (self.audio_playback_button_rect.bottom): 
                self.AUDIO_BUTTON = True

class PartialTouch(Touch):
    def __init__(self):
        Touch.__init__(self)

        #creating exit button
        self.exit_button_x_offset = 300
        self.exit_button_y_offset = 370
        self.exit_button = pygame.image.load('button background.png')
        self.exit_button_rect = self.exit_button.get_rect()
        self.exit_button_rect.topleft = (self.exit_button_x_offset, self.exit_button_y_offset)

    def touch_draw(self, display):

        #display exit button
        display.blit(self.exit_button, self.exit_button_rect)
        self.exit = self.draw_text(display, 'EXIT', 15, self.exit_button_rect.centerx, self.exit_button_rect.centery, "center")
        
    def touch_input(self, finger):

        if (self.exit_button_rect.left) <= finger['x'] <= (self.exit_button_rect.right):
            if (self.exit_button_rect.top) <= finger['y'] <= (self.exit_button_rect.bottom): 
                self.EXIT_BUTTON = True
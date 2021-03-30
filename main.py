from functions import *

curr_function = Functions()

curr_function.main_menu()

while curr_function.running:

    if curr_function.main_flag:
        curr_function.main_flag = False
        curr_function.main_running = True
        curr_function.main_menu()

    if curr_function.frequency_flag:
        curr_function.frequency_flag = False
        curr_function.frequency_running = True
        curr_function.frequency_analysis_function()

    if curr_function.word_flag:
        curr_function.word_flag = False
        curr_function.word_running = True
        curr_function.word_recognition_function()

    if curr_function.person_flag:
        curr_function.person_flag = False
        curr_function.person_running = True
        curr_function.person_detection_function()

    if curr_function.audio_flag:
        curr_function.audio_flag = False
        curr_function.audio_running = True
        curr_function.audio_playback_function()
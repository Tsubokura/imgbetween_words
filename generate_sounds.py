import mido
import datetime
import cv2
import time
import numpy as np
from mido import Message, MidiFile, MidiTrack, MetaMessage

def generate_sounds(vector_fromwords, imgname):

    array_fromwords = np.array(vector_fromwords)
    rowsize_array, culumsize_array = array_fromwords.shape
    img = cv2.imread(imgname, 0)
    height_img, width_img = img.shape

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    midi_deafultgradiation = 127
    track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))

    for index_row in range(rowsize_array):
        # "array_fromwords" + str(index_row)= [array_fromwords[index_row][index_culum] for index_culum in range(culumsize_array)]
        array_fromwords_first = [array_fromwords[0][index_culum] for index_culum in range(culumsize_array)]
        array_fromwords_secound = [array_fromwords[1][index_culum] for index_culum in range(culumsize_array)]
        array_fromwords_third = [array_fromwords[2][index_culum] for index_culum in range(culumsize_array)]
        array_fromwords_forth = [array_fromwords[3][index_culum] for index_culum in range(culumsize_array)]
        array_fromwords_fifth = [array_fromwords[4][index_culum] for index_culum in range(culumsize_array)]
        #1 : concrete 2 : karm 3 : sad 4 : beautiful 5: vivid


    firstwords_value = min(np.mean(array_fromwords_first) * 5, 1)
    secoundwords_value = min(np.mean(array_fromwords_secound) * 2, 1)
    thirdwords_value = min(np.mean(array_fromwords_third) * 2, 1)
    forthwords_value = min(np.mean(array_fromwords_forth) * 2, 1)
    fifthwords_value = min(np.mean(array_fromwords_fifth) * 2, 1) #動的変数生成は諦めた

    # firstwords_value = 0
    # secoundwords_value = 0
    # thirdwords_value = 0
    # forthwords_value = 0
    # fifthwords_value =0

    # for index in range(width_img * height_img):
    #     velocity_list.append( int( 127( 1 - np.random.rand() * secoundwords_value) ) )
    #     interval_list.append( int( 100( 1 - abs(np.random.randn()) * thirdwords_value) ) )

    print(firstwords_value)
    print(secoundwords_value)
    print(thirdwords_value)
    print(forthwords_value)
    print(fifthwords_value)

    sharpvalue_list = [1, 3, 6, 8, 10, 13, 15, 18, 20, 22, 25, 27, 30, 32, 34, 37, 39, 42,
                44, 46, 49, 51, 54, 56, 58, 61, 63, 66, 68, 70, 73, 75, 78, 80, 82, 85,
                87, 90, 92, 94, 97, 99, 102, 104, 106, 109, 111, 114, 118, 121, 123, 126] # sharp values

    max_interval = 300
    max_velocity = 127
    velocity_space = 32
    interval_space = 32

    interval_basetime = 150
    velocty_basesize  = 127

    if(secoundwords_value != 0):
        interval_list = [min ( int ( abs( np.random.rand() * 200)), max_interval) for index in range(interval_space)]
    else :
        interval_list = [100 for index in range(interval_space)]

    if(thirdwords_value != 0):
        velocity_list = [min ( int ( abs( np.random.rand() ) * 100 ), max_velocity) for index in range(velocity_space)]
    else :
        velocity_list = [100 for index in range(interval_space)] #諦めた

    # print(interval_list)
    # print(velocity_list)

    # velocity_list = [int( velocty_basesize * ( 1 - np.random.rand() * secoundwords_value) ) for index in range(width_img * height_img)]
    # interval_list = [int( interval_basetime * abs(( 1 - abs(np.random.rand()) * thirdwords_value)) ) for index in range(width_img * height_img)]
    interval_velocity_count = 0

    for x_value in range(width_img -1):
        for y_value in range(height_img  -1):

            if(interval_velocity_count == 0):
                note_value = img[y_value][x_value]

            #note_value = int(img[y_value][x_value] * abs(np.random.rand() * (1 - fifthwords_value) ) ) % midi_deafultgradiation
            note_value = int(img[y_value][x_value] + ((note_value - img[y_value][x_value]) * np.random.rand() * 10 * fifthwords_value) ) % midi_deafultgradiation
            chord_notevalue_first = (note_value + int(fifthwords_value * np.random.rand() * 10) ) % midi_deafultgradiation
            chord_notevalue_second = (note_value + int(fifthwords_value * np.random.rand() * 10) ) % midi_deafultgradiation

            if(forthwords_value * (interval_velocity_count % 100) > 1): # 確率的に半音を削除するかどうかを決める
                if(note_value in sharpvalue_list):
                    note_value -= 1

                if(chord_notevalue_first in sharpvalue_list):
                    chord_notevalue_first -= 1

                if(chord_notevalue_second in sharpvalue_list):
                    chord_notevalue_second -= 1

            if (interval_velocity_count % interval_space == 0 and secoundwords_value != 0):
                interval_list = [min(int( secoundwords_value * (int(interval_list[index] + abs( np.random.randn()  + 50) )) ), max_interval )  for index in range(interval_space)]

            if (interval_velocity_count % velocity_space == 0 and thirdwords_value != 0):
                velocity_list = [min(int( thirdwords_value * (int(velocity_list[index] + np.random.rand() * 20) ) ), max_velocity )for index in range(velocity_space)]

            interval_velocity_count += 1
            index_interval_velocity_count = interval_velocity_count % velocity_space

            if(0 <= firstwords_value and firstwords_value < 0.3):
                track.append(Message('note_on', note=note_value, velocity=velocity_list[index_interval_velocity_count], time=0))
                track.append(Message('note_off', note=note_value, velocity=velocity_list[index_interval_velocity_count], time=interval_list[index_interval_velocity_count] ))


            elif(0.3 <= firstwords_value and firstwords_value < 0.7):
                track.append(Message('note_on', note=note_value, velocity=velocity_list[index_interval_velocity_count], time=0))
                track.append(Message('note_on', note=chord_notevalue_first, velocity=velocity_list[index_interval_velocity_count], time=0))

                track.append(Message('note_off', note=note_value, velocity=0, time=interval_list[index_interval_velocity_count] ))
                track.append(Message('note_off', note=chord_notevalue_first, velocity=0, time=interval_list[index_interval_velocity_count] ))

            else:
                track.append(Message('note_on', note=note_value, velocity=velocity_list[index_interval_velocity_count], time=0))
                track.append(Message('note_on', note=chord_notevalue_first, velocity=velocity_list[index_interval_velocity_count], time=0))
                track.append(Message('note_on', note=chord_notevalue_second, velocity=velocity_list[index_interval_velocity_count], time=0))

                track.append(Message('note_off', note=note_value, velocity=100, time=interval_list[index_interval_velocity_count]))
                track.append(Message('note_off', note=chord_notevalue_first, velocity=100, time=interval_list[index_interval_velocity_count]  ))
                track.append(Message('note_off', note=chord_notevalue_second, velocity=100, time=interval_list[index_interval_velocity_count] ))


            #print(velocity_list)

            # if(0 <= firstwords_value and firstwords_value < 0.3):
            #     track.append(Message('note_on', note=note_value, velocity=velocity_list[index_interval_velocity_count], time=interval_list[index_interval_velocity_count] ))
            #     track.append(Message('note_off', note=note_value, velocity=velocity_list[index_interval_velocity_count], time=interval_list[index_interval_velocity_count] ))
            #
            # elif(0.3 <= firstwords_value and firstwords_value < 0.7):
            #     track.append(Message('note_on', note=note_value, velocity=velocity_list[index_interval_velocity_count], time=interval_list[index_interval_velocity_count] ))
            #     track.append(Message('note_on', note=chord_notevalue_first, velocity=velocity_list[index_interval_velocity_count], time=interval_list[index_interval_velocity_count] ))
            #
            #     track.append(Message('note_off', note=note_value, velocity=0, time=interval_list[index_interval_velocity_count] ))
            #     track.append(Message('note_off', note=chord_notevalue_first, velocity=0, time=interval_list[index_interval_velocity_count] ))
            #
            # else:
            #     track.append(Message('note_on', note=note_value, velocity=velocity_list[index_interval_velocity_count], time=interval_list[index_interval_velocity_count] ))
            #     track.append(Message('note_on', note=chord_notevalue_first, velocity=velocity_list[index_interval_velocity_count], time=interval_list[index_interval_velocity_count] ))
            #     track.append(Message('note_on', note=chord_notevalue_second, velocity=velocity_list[index_interval_velocity_count], time=interval_list[index_interval_velocity_count] ))
            #
            #     track.append(Message('note_off', note=note_value, velocity=velocity_list[index_interval_velocity_count], time=0 ))
            #     track.append(Message('note_off', note=chord_notevalue_first, velocity=velocity_list[index_interval_velocity_count], time=0 ))
            #     track.append(Message('note_off', note=chord_notevalue_second, velocity=velocity_list[index_interval_velocity_count], time=0 ))

    now = datetime.datetime.now()
    midifile_name = 'new_song_' + now.strftime('%Y%m%d_%H%M%S') + '.mid'
    mididir_name = './output_sounds/'
    mid.save(mididir_name + midifile_name)

    ports = mido.get_output_names()
    with mido.open_output(ports[0]) as outport:
        for msg in mido.MidiFile(mididir_name + midifile_name):
            time.sleep(msg.time)
            if not msg.is_meta:
                print(outport, msg)
                outport.send(msg)

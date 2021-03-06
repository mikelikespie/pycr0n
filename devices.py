import pygame
from processing import Process, Pipe
from config import *
import launchpad
import logitech as lt
import gradient

global launchpad_in, launchpad_out, nanokontrol_in, yoke1, yoke2, yoke3, yoke6, yoke7, yoke8

# Clear Launchpad
print "\n","Clearing...","\n"
for i in xrange(8):
    launchpad.clear(i)

def poll():
    global sparsity
    if launchpad_in.poll():
        data = launchpad_in.read(1)
        control = data[0][0][0]
        note = data[0][0][1]
        velocity = data[0][0][2]

        if velocity == 127:
            if control == 176:
                launchpad.clear(note - 104)
            elif note%16 < 8:
                launchpad.toggle(note)
         
            elif note%16 == 8:
                launchpad.rand((note-8)/16)


    if gradient.parent.poll():
        data = gradient.parent.recv()
        print data
        if data[0] == 8:
            sparsity = data[0]
        elif data[0] > 23 and data[0] < 32:
            launchpad.armed[data[0] - 24] = data[1]/127

    # nanokontrol CCs all on channel 0
    # knobs 16-23
    # sliders 0-7
    # solo 32-39
    # mute 48-55
    # rec 64-71
    # rew 43
    # ff 44
    # stop 42
    # play 41
    # record 45
    # cycle 46
    # set left right 60-62
    # trackleft trackright 58-59

    if nanokontrol_in.poll():
        data = nanokontrol_in.read(1)
        note = data[0][0][1]
        velocity = data[0][0][2]
        if (note > 31 and note < 40):
            midiout(note=note,velocity=127,channel=12,device=yoke3)
        elif (note > 47 and note < 56):
            midiout(note=note, velocity=127 if velocity == 0 else 0, channel=12,device=yoke3)
        elif (note > 63 and note < 72):
            midiout(note=note,velocity=127,channel=12,device=yoke3)
        
        else:
            midiout(note=note,velocity=velocity,channel=12,device=yoke3)

    #global lt.pad_state, lt.axis2_state
    pygame.event.pump()
    if pygame.event.peek(pygame.JOYBUTTONDOWN):
        pygame.event.clear()
        for i in xrange(12):
            if lt.logitech_in.get_button(i):
                if i == 0:
                    midiout(note=0,velocity=127,channel=13,device=yoke3)
    if pygame.event.peek(pygame.JOYBUTTONUP):
        pygame.event.clear()
        print "pushUP!",lt.logitech_in.get_button(0)
    if pygame.event.peek(pygame.JOYHATMOTION):
        pygame.event.clear()
        print "left stick!",lt.logitech_in.get_hat(0)
    if pygame.event.peek(pygame.JOYAXISMOTION):
        tmp1 = lt.logitech_in.get_axis(0)
        tmp2 = lt.logitech_in.get_axis(2)/8
        pygame.event.clear()
        if (lt.axis2_state != tmp1) and lt.logitech_in.get_button(10):
            lt.axis2_state = tmp1
            launchpad.push_params(lt.axis2_state + lt.axis3_state)
        elif (lt.axis3_state != tmp2) and lt.logitech_in.get_button(11):
            lt.axis3_state = tmp2
            launchpad.push_params(lt.axis2_state + lt.axis3_state)


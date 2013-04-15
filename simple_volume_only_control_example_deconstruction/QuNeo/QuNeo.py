# VERSION 1.0

# Copyright 7/3/2012
# Control Surface Remote Script Created by Alex Molina 
# for QuNeo 3D MultiTouch Pad Controller by Keith McMillen Instruments
# TESTED DEVICE = QUENEO SERIAL #104998

from __future__ import with_statement # live9 forward compatibility

import Live
import time

from _Framework.ControlSurface import ControlSurface # @marwei -- this instance is passed in to the main class
from _Framework.InputControlElement import * # needed and is associated with MIDI_CC_TYPE
from _Framework.SliderElement import SliderElement # @marwei required

#from SpecialSessionComponent import SpecialSessionComponent #required #========

from SpecialMixerComponent import SpecialMixerComponent #required keeping the subclass pattern

# temp vars killing MIDI map to be move to parameters.py

# NEW
gutter = 3 # track offset. Int will push script ot the right and leave a left gutter
track_volume = [1, 2, 3, 4] # the CC's

# existing
# midi_channel is offset below. Range begins at 1, not 0. Thus assigning 1 here will snd 0 to the machine
midi_channel=1
# Offsetting compensation next
midi_channel -= 1  # << Do not remove this inless you understand the consequences
box_width = 4 # width of the the "red-box" aka tracks
box_height = 4 #height of the "red-box" aka scenes


class QuNeo(ControlSurface):
    __doc__ = " Minimal Script for Volume control via _Framework by @djnsm / Data Mafia "
    __module__ = __name__
    
    # INIT FUNCTION FOR QUNEO   
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance) # in aaa
        with self.component_guard(): # new for Live9 / Py
          self._suppress_session_highlight = True
          self._suppress_send_midi = True
       #   self.session = None #===========
          self.mixer = None
          self.box_width = box_width
         # self.transport = None -----marwei
         # self.led_value = None ------marwei
          #self._note_input = [] -------marwei
          
          # marwei added for web app++
          self.gutter = gutter # see param info
 
          self.volume_control = None
 
          self._setup_mixer_control() #------- needed
          #self._setup_session_control() # -----------
          #self.session.set_mixer(self.mixer) #----------
 
          # @marwei --- needed? 8apr
          self._suppress_session_highlight = False
                  
    # DISCONNECT FUNCTION
    def disconnect(self):
        self.mixer
        self.session
            
       #self._note_input = None
        ControlSurface.disconnect(self)
        return None

    
    # CREATE A SLIDER @marwei reqd
    def slider(self, channel, value):
        if (value != -1):
            return SliderElement(MIDI_CC_TYPE, channel, value)
        else:
            return None
            
            
    # REASSIGN MIXER
    def _reassign_mixer_control(self, shift_value):
        self.volume_control = self.slider(midi_channel, SELECTED_VOL)
        if (self.volume_control != None):
            self.mixer.selected_strip().set_volume_control(self.volume_control)
        else:
            self.mixer.selected_strip().set_volume_control(None)
    
    # SETUP MIXER
    def _setup_mixer_control(self):
        
        self.mixer = SpecialMixerComponent(self.box_width, self) # get a local mixer object ready
        self.mixer.name = 'Mixer' # name
        self.mixer.set_track_offset(self.gutter)  # gutter ----marwei
        # compare width with track vol count to qualify -- put somewhere else 
        for index in range(self.box_width): # @marwei must kill this style and count
            self.mixer.channel_strip(index).set_volume_control(self.slider(midi_channel, track_volume[index]))
            
from rpi_ws281x import *
import vlc
import time

def sunrise(strip):
  """
    Mimic the sunrise by starting LEDs at a dark navy color, then changing to red, and finally to yellow. This
    function can be reversed for a sunset function! Nature sure is neat, huh?
  """
  
  # initialize the media player
  player = vlc.MediaPlayer("/home/pi/forest_alarm.mp3")

  # set the colors of each phase
  BLUE_PHASE   = [0, 0, 2]
  RED_PHASE    = [20, 0, 0]
  YELLOW_PHASE = [255, 255, 0]

  # initialize empty array to be used for the deltas
  phase1_delta = [0, 0, 0]
  phase2_delta = [0, 0, 0]

  # initialize other vars
  curr_color = BLUE_PHASE
  curr_time  = 0
  duration   = 1200
  time_delay = 0.25

  # define the deltas in both phases of the sunrise function - trying to squeeze a teeny bit of speed by 
  # unwrapping a small for loop
  phase1_delta[0] = (RED_PHASE[0] - BLUE_PHASE[0])/((duration/time_delay)/2)
  phase1_delta[1] = (RED_PHASE[1] - BLUE_PHASE[1])/((duration/time_delay)/2)
  phase1_delta[2] = (RED_PHASE[2] - BLUE_PHASE[2])/((duration/time_delay)/2)
  phase2_delta[0] = (YELLOW_PHASE[0] - RED_PHASE[0])/((duration/time_delay)/2)
  phase2_delta[1] = (YELLOW_PHASE[1] - RED_PHASE[1])/((duration/time_delay)/2)
  phase2_delta[2] = (YELLOW_PHASE[2] - RED_PHASE[2])/((duration/time_delay)/2)

  try:
    # start the alarm sound
    player.play()
    while curr_time < duration:
      if (curr_time < duration/2):
        # unwrapping loops seems hacky :( but it's supposed to be faster
        curr_color[0] += phase1_delta[0]
        curr_color[1] += phase1_delta[1]
        curr_color[2] += phase1_delta[2]
      else:
        # unwrapping loops seems hacky :( but it's supposed to be faster
        curr_color[0] += phase2_delta[0]
        curr_color[1] += phase2_delta[1]
        curr_color[2] += phase2_delta[2]
      for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, Color(int(curr_color[0]), int(curr_color[1]), int(curr_color[2])))
      strip.show()
      curr_time += time_delay
      time.sleep(time_delay)

  finally:
    # stop the alarm sound
    player.stop()
    for i in range(0, strip.numPixels()):
      strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

if __name__ == '__main__':

  strip = PixelStrip(100, 10)
  strip.begin()
  sunrise(strip)
  

import time
from random import randint
from rpi_ws281x import Color, PixelStrip

# Define the default IO pin and number of pixels in the LED array
GPIO_PIN   = 18
NUM_PIXELS = 1

class Lights:
  """
    The Lights class will define all possible functions for the LEDS. So far, modes and power can be set for the LED
    array.
  """

  def __init__(self, num_pixels=NUM_PIXELS):
    """
      Initialize our Lights class. On initialization, default values are set, and processing for the strip will
      begin.
    """

    self.num_pixels = num_pixels
    self.strip      = PixelStrip(self.num_pixels, 18)
    self.power      = False
    self.strip.begin()

  def clear(self):
    """
      Clear the existing LED array. This will set all LEDs in the array to a blank color (this is the power off
      function).
    """

    for i in range(0, self.num_pixels):
      self.strip.setPixelColor(i, Color(0, 0, 0))
    self.strip.show()

  def arcade(self, duration):
    """
      The arcade function will define a set of chasing lights. When the next light in the array is powered on, the 
      previous light is powered off.
    """

    curr_time = 0
    delay = 0.2

    # try-except-finally defined so that the LED array is ALWAYS powered off on exit (finally is always executed)
    try:
      while curr_time < duration:
        for i in range(0, self.num_pixels):
          strip.setPixelColor(i, Color(255, 255, 255))
          # this conditional handles whether the first light is turned on or not; if the first light is on,
          # then the last light must be powered off
          if i > 0:
            strip.setPixelColor(i-1, Color(0, 0, 0))
          else:
            strip.setPixelColor(self.num_pixels - 1, Color(0, 0, 0))
          strip.show()
          time.sleep(delay)
          curr_time += delay
    finally:
      self.clear()

  def ambient(self, duration):
    """
      The ambient function will slowly change the colors of individual LEDs. Using the random function allows for a
      random R, G, or B value to be changed so that each LED has a unique color.
    """

    curr_color = []
    curr_time  = 0
    delay = 0.2
    incr  = 1

    # a list of all colors must be kept (and updated) for the ambient animation to work
    for i in range(0, self.num_pixels):
      curr_color.append([0, 0, 0])

    # try-except-finally defined so that the LED array is ALWAYS powered off on exit (finally is always executed)
    try:
      while curr_time < duration:
        for i in range(0, self.num_pixels):
          # Address, randomly, a red, green, or blue value, i is the pixel number, j is the color component
          j = randint(0, 2)
          if curr_color[i][j] >= 245:
            curr_color[i][j] -= 10
            incr = -1
          elif curr_color[i][j] <= 10:
            curr_color[i][j] += 10
            incr = 1
          else:
            curr_color[i][j] += (10 * incr)
          self.strip.setPixelColor(i, Color(curr_color[i][0], curr_color[i][1], curr_color[i][2]))
          self.strip.show()
        time.sleep(delay)
        curr_time += delay
    finally:
      self.clear()

  def christmas(self, duration):
    """
      It's that time of year again (it's always that time; don't @ me). The christmas function will alternate green
      and red lights.
    """
   
    RED   = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)

    mode1 = RED
    mode2 = GREEN
    curr_time = 0
    delay = 0.25

    # try-except-finally defined so that the LED array is ALWAYS powered off on exit (finally is always executed)
    try:
      while curr_time < duration:
        for i in range(0, self.num_pixels):
          # even LEDs set to mode1
          if i%2 == 0:
            self.strip.setPixelColor(i, mode1)
          # odd LEDs set to mode2
          else:
            self.strip.setPixelColor(i, mode2)
        self.strip.show()
        # swap the color mode being used (on each iteration, red LEDs should turn green and vice versa)
        temp_mode = mode1
        mode1 = mode2
        mode2 = temp_mode
        curr_time += delay
        time.sleep(delay)
    finally:
      self.clear()
    
  def set_power(self, power):
    """
      Set power will turn on or off the module (depending on it's current power state). This just set's power to 
      the opposite of itself and either gives white light or clears the array.
    """

    if not self.power:
      # establish that the LEDs are currently powered on
      self.power = True
      for i in range(0, self.num_pixels):
        self.strip.setPixelColor(i, Color(255, 255, 255))
      self.strip.show()
    else:
      # establish that the LEDs are currently powered off
      self.power = False
      self.clear()

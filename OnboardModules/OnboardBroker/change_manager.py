from Lights.lights import Lights
from AlarmClock.alarmClock import AlarmClock

class ChangeManager:

  def __init__(self):
    lights = Lights(100)
    alarm  = AlarmClock()
    print("Light and Alarm Clock initialized")

  def set_change(self, var, action_data):
    print("Changing Var . . .")
    if var.upper == 'MODE':
      lights.set_mode(action_data)
    elif var.upper == 'TIME':
      alarm.set_alarm_time(action_data)
    print("{} set to {}.".format(var, action_data))
    

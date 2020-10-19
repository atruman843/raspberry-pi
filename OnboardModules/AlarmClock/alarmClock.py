from crontab import CronTab

# Set the default value for alarm time and the days on which it will ring  
ALARM_TIME = "07:00"
ALARM_DAYS = [1, 2, 3, 4, 5, 6, 7]

class AlarmClock:
  """
    The AlarmClock class will allow users to control certain aspects of the alarm clock. Currently the only
    function is to set the time for an alarm to go off.
  """

  def __init__(self):
    """
      Simple init function. Nothing is set here.
    """

    print("New Alarm Clock created")

  def set_alarm_time(self, time=ALARM_TIME, days=ALARM_DAYS, wakeup_interval=2):
    """
      The set_alarm_time function creates a cron job to run at the specified time on the specified days.
      The wakeup_interval defines the period over which the user will be woken up. Functionality for this will
      be extended in the future.
    """

    try:
      # remove any previous cron jobs; this functionality will need to be specified so that multiple alarms
      # can be set
      cron.remove_all()
      # gets an array where the first indexed item is the hour of the day, and the second indexed item is the 
      # minute
      hour_and_minute = time.split(":")
      # we want to start the alarm before our intended wakeup time
      hour_and_minute[0] -= wakeup_interval
      cron = CronTab(user=True)
      job = cron.new(command='sudo python3 /home/pi/raspberry-pi/OnboardModules/AlarmClock/alarm.py >> /home/pi/output.txt')
      job.hour.on(hour_and_minute[0])
      job.minute.on(hour_and_minute[1])
      for i in days:
        job.day.on(i)
      cron.write()
      print("Cron job created successfully")

    except:
      print("Cron job could not be created")


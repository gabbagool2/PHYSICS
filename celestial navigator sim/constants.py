import json
import os

#waypoints = expected coordinates
with open('coordinates.json', 'r') as file:
    WAYPOINTS = json.load(file)

#sailor always takes  reading at 3pm therefor 3 hours after noon 3*15 = 45 degrees
TIME_SIGHT = 45.0000

#starting point of daily sun declination
STARTING_DECLINATION = 10.0000

#daily increment of change in declination
DAILY_DECLINATION_SHIFT = -0.3000

MAX_DEC_DAYS = 100

# so sailor lands within nautical mile range 
SUCCESS_THRESHOLD_DEGREES = 80.0 / 60.0  # roughly 1.3333 degrees

#finds current days declination
declinations = []
for day in range(MAX_DEC_DAYS):
    current_declination = STARTING_DECLINATION+(day*DAILY_DECLINATION_SHIFT)
    declinations.append(current_declination)




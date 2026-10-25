"""
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

simulation of navigating via the stars on an old ship in the 1800s

based off of the noon sight and time sight method.

these methods picked as contain least amount of external variables
and those that are there are easily fixed with some assumptions

-no actual date system implemented, therefor the sun declination is 
found by assuming it starts at 10 degrees on day 1 and increments -0.3 
degrees every day. (typical range of declination between approx +-24 degrees).
program assumes 100 days ie 100 declinations. 

-GHA greenich angle assumed to to be fixed for time sight method (therefor 
its as if the sailor was taking the reading at exactly the same time every 
day a few hours after noon.)

-1800s ship would travel approx 100-150nm  day depending on conditions of the sea.
we ignore all sea conditions and assume they travel about 150-200nm (this was 
to account for the amount of plots on the planned journey, they are not precise 
so we make the assumption that it travels this much every day) HOWEVER, Note time
is not recorded...

-for time the system is as follows. one day = one sun declination reading =one 
reading of longitude and latitude = the approximation of 150-200nm. after 100 
days they run out of supplies and are considered lost at sea.

-if a sailor is within 80nm of its target it maintains course as normal and 
attempts for the next position/day. if a sailor is outwith the 80nm target 
then they waste a day "re-rolling" with another reading for the position they missed

- readings are calculated as follows. 
target coordinates grabbed for sailor -> coordinates reversed to obtain 
expected angle sailor would record on sextant -> sailors % error added to the 
expected angle -> flawed coordinates passed back through the original noon/time 
sight formula to find flawed coordinates.

-The simulation does not distinguish between land or sea, hence why the literal
flying dutchman may appear on your google earth plot.

- to try with your own journey you must plot a journey on google earth with the 
polgon feature. Once you do this you can export a KML file that containts the coordinates. 
open the kml with a text editor and copy the coordinates. Calculate them from decimal to 
true degrees and then input them in the coordinates.json file. (i recommend using a small 
python function or ai to do it for you as it is tedious filling each long/lat in). once your
coordinates are as the coordinates in the original coordinates.json it should run fine. To 
change the error margin on each sailor (ie the % chance theyll miss.) just alter it at the roster
at the bottom (anything over 4-6% will be chaos - these kinds of erros end up covering ranges of 
hundreds of miles). Once the simulation has run it will output the results in the terminal. If you 
wish to see the plots you extract the KML files the program creates and upload them to google earth

enjoy :)

Note - Gemini AI assisted in writing this code with particular attention to the exporter and coordinate files, converting
all 43 coordinates from decimal to degrees and formatting of output to the terminal.

algorithm was written by Luke Sherrington, using the formulas and methods fromthe paper 
" a short guide to celestial naviation" by Henning Umland - 15/03/19 &
"AMERICAN PRACTICAL NAVIGATOR - AN EPITOME OF NAVIGATION Volume 1 and 2"
by nathanial bowditch - 2024

"""








import math
import random
import constants
import exporter

# finds expected angle for sailor to record on his sextant
def find_ho(expected_lat, declination):
    
    # finds zenith distance
    z = abs(expected_lat - declination)
    
    # finds expected sextant angle for latitude
    ho = 90 - z
    
    return ho



# calculates the latitude using the new % error ho reading
def find_lat(Ho, declination, expected_lat):
    
    # finds zenith distance
    z = 90 - Ho
    
    # equator check - if i am north of the sun i must be facing south
    if expected_lat > declination:
        lat = declination + z

    # if i am south of the sun i must be facing north
    else:
        lat = declination - z

    # returns the value for latitude
    return lat



# finds expected angle for sailor to record on his sextant and his chronometer
def find_h(expected_lat, declination):
    
    # degrees to radians
    lat_rad = math.radians(expected_lat)
    dec_rad = math.radians(declination)
    t_rad = math.radians(constants.TIME_SIGHT)

    sin_h = (math.cos(t_rad) * math.cos(lat_rad) * math.cos(dec_rad)) + \
            (math.sin(lat_rad) * math.sin(dec_rad))
    
    # rad to degrees
    h = math.degrees(math.asin(sin_h))
    
    # returns expected sailor reading to find lon
    return h



# finds lontitude using the % error h reading
def find_lon(h, lat, declination, GHA, expected_lon):
    
    # degrees to radians
    H_rad = math.radians(h)
    lat_rad = math.radians(lat)
    dec_rad = math.radians(declination)
    
    # handles formula for t (meridian angle)
    t_frac = (math.sin(H_rad) - (math.sin(lat_rad) * math.sin(dec_rad)))/(math.cos(lat_rad) * math.cos(dec_rad))
    # adds bounds incase domain errors caused by % error debuff
    t_frac = max(-1, min(1, t_frac))
    # finishes formula for t and converts back to degrees
    t = math.degrees(math.acos(t_frac))

    # find lon1/lon2 and check if it is correct lon reading
    lon1 = t - GHA
    lon2 = 360 - t - GHA

    if lon1 < -180:
        lon1 += 360
    if lon1 > 180:
        lon1 -= 360
    if lon2 < -180:
        lon2 += 360
    if lon2 > 180:
        lon2 -= 360

    if abs(expected_lon - lon1) < abs(expected_lon - lon2):
        return lon1
    else:
        return lon2



# applys the % error to the angles 
def error(angle, error_percent):

    #sets range for error range ie +-%
    random_error = random.uniform(-error_percent, error_percent)
    error_angle = angle * (1 + random_error)
    #returns flawed angle
    return error_angle


#handles checking the turn back condition
def turn_back_check(lat, lon, expected_lat, expected_lon):
    
    # a2+b2=c2 pythagorean theroem for finding straight line distance on flat grid between true and error position
    distance_off_deg = math.sqrt((expected_lat - lat)**2 + (expected_lon - lon)**2)
    
    # 1degree lat = 60nm, converts the celestial degrees into tangible real world distance
    distance_off_nm = distance_off_deg * 60.0
    
    #returns distance sailor is off of original point
    return distance_off_nm


#main sim function
def run(sailors):
    
    print("\n\n|||| start |||||\n\n")
    current_day = 0
    
    # The race continues until all sailors finish or declination data runs out approx 100 days
    while any(not s['finished'] for s in sailors) and current_day < len(constants.declinations):
        
        current_dec = constants.declinations[current_day]
        print(f"\n{'='*60}")
        print(f"DAY {current_day + 1} (Sun Declination: {current_dec:.4f}°)")
        print(f"{'='*60}")

        # Let every sailor take their daily reading
        for sailor in sailors:
            # Skip sailors who have already reached Cape Town
            if sailor['finished']:
                continue

            target_index = sailor['target_index']
            
            # Grab true variables for this specific sailor's target
            true_lat = constants.WAYPOINTS[target_index]['lat']
            true_lon = constants.WAYPOINTS[target_index]['lon']
            
            perfect_GHA = constants.TIME_SIGHT - true_lon
            if perfect_GHA > 360: perfect_GHA -= 360
            if perfect_GHA < 0: perfect_GHA += 360
            
            perfect_ho = find_ho(true_lat, current_dec)
            perfect_h = find_h(true_lat, current_dec)
            
            # Apply THIS sailor's specific error margin
            flawed_ho = error(perfect_ho, sailor['error_margin']) 
            flawed_h = error(perfect_h, sailor['error_margin'])
            
            error_lat = find_lat(flawed_ho, current_dec, true_lat)
            error_lon = find_lon(flawed_h, error_lat, current_dec, perfect_GHA, true_lon)
        
            # Check their distance
            distance_off_nm = turn_back_check(error_lat, error_lon, true_lat, true_lon)
            sailor['total_distance_missed'] += distance_off_nm
            
            # for KML to plot route on GE
            sailor['track'].append(f"{error_lon:.5f},{error_lat:.5f},0")
            
            # Print their daily attempt
            print(f"{sailor['name']} (Aiming for P{target_index + 1})")
            print(f"   True Coords:  Lat {true_lat:.2f}, Lon {true_lon:.2f}")
            print(f"   Calculated:   Lat {error_lat:.2f}, Lon {error_lon:.2f} (Missed by {distance_off_nm:.1f} nm)")
            
            if distance_off_nm <= 80.0:
                print("   -> SUCCESS! Sailed to the next waypoint.")
                sailor['target_index'] += 1  
                # Check if they just hit the final waypoint (Cape Town)
                if sailor['target_index'] == len(constants.WAYPOINTS):
                    sailor['finished'] = True
                    sailor['total_days'] = current_day + 1
            else:
                print("   -> FAILED! Too far off course. Wasted a day.")
                sailor['wasted_days'] += 1   
            
            print("-" * 60)

        # The sun sets, next day begins
        current_day += 1

    # --- FINAL STATS BOARD ---
    print("|||||||||||||||||||||||||||||||||||")
    print("RACE RESULTS: ARRIVAL IN CAPE TOWN ")
    print("|||||||||||||||||||||||||||||||||||\n\n")
    
    for sailor in sailors:
        # Determine how many days they actually sailed to calculate the average
        days_sailed = sailor['total_days'] if sailor['finished'] else current_day
        avg_miss_distance = sailor['total_distance_missed'] / days_sailed if days_sailed > 0 else 0
        if sailor['finished']:
            print(f"{sailor['name']}")
            print(f"   Total Days at Sea: {sailor['total_days']}")
            print(f"   Days Wasted (Got Lost): {sailor['wasted_days']}\n")
        else:
            print(f"{sailor['name']} (Lost at Sea!)")
            print(f"Ran out of supplies on Day {current_day} trying to find P{sailor['target_index'] + 1}\n")
        print(f"   Days Wasted (Got Lost): {sailor['wasted_days']}")
        print(f"   Average Miss Distance:  {avg_miss_distance:.1f} nm per day\n")



if __name__ == "__main__":
    
    # Create the roster of sailors racing each other
    fleet = [
        {"name": "HMS Victory", "error_margin": 0.0085, "target_index": 0, "wasted_days": 0, "finished": False, "total_days": 0, "track": [], "total_distance_missed": 0},
        {"name": "HMS Trafalgar", "error_margin": 0.01, "target_index": 0, "wasted_days": 0, "finished": False, "total_days": 0, "track": [], "total_distance_missed": 0},
        {"name": "HMS Waterloo", "error_margin": 0.03, "target_index": 0, "wasted_days": 0, "finished": False, "total_days": 0, "track": [], "total_distance_missed": 0},
        {"name": "HMS Centurion", "error_margin": 0.05, "target_index": 0, "wasted_days": 0, "finished": False, "total_days": 0, "track": [], "total_distance_missed": 0},
        {"name": "HMS Albion", "error_margin": 0.1, "target_index": 0, "wasted_days": 0, "finished": False, "total_days": 0, "track": [], "total_distance_missed": 0},
        {"name": "HMS Majestic", "error_margin": 0.30, "target_index": 0, "wasted_days": 0, "finished": False, "total_days": 0, "track": [], "total_distance_missed": 0}
    ]

    # Run the simulation
    run(fleet)
    
    # Export the maps
    exporter.export_kml(fleet)
   
            
def pace(distance, minutes, seconds):
            print("Minutes: ",(minutes))
            print("Seconds: ",(seconds))
            mins_in_seconds = (int(minutes))*60
            print("Minutes in seconds: ", mins_in_seconds)
            time = mins_in_seconds + int(seconds)
            print("Total Time", time)
            pace_in_seconds = int(time/float(distance))
            print("Pace in seconds: ",pace_in_seconds)
            pace_in_mins = str(float(pace_in_seconds/60)).split(".")
            print("Pace in mins as decimal list: ",pace_in_mins)

            if len(pace_in_mins) == 1:
                print("One item in list")
                pace_in_mins.append("00")
            else:
                print("Two items in list")
                pace_in_mins[1] = str(int(60*float("0."+pace_in_mins[1])))
                print("seconds: ",pace_in_mins[1])
            
            pace = f'{pace_in_mins[0]}:{pace_in_mins[1]}'
            return pace
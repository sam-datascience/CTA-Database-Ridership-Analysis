import sqlite3
import matplotlib.pyplot as figure

#
# main
#

def printstats():         # function to print the stats before the user prompt
  dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
  dbCursor = dbConn.cursor()

  sql = """Select count(Station_ID)
         From Stations;"""
  dbCursor.execute(sql)
  row = dbCursor.fetchone()
  print('** Welcome to CTA L Analysis app **')
  print()
  print('General Stats: ')
  print("  # of stations:", f"{row[0]:,}")

  sql = """Select count(Stop_ID)
          From Stops;"""
  dbCursor.execute(sql)
  row = dbCursor.fetchone()
  print("  # of stops:", f"{row[0]:,}")

  sql = """Select count(Num_Riders)
          From Ridership;"""
  dbCursor.execute(sql)
  row = dbCursor.fetchone()
  print("  # of ride entries:", f"{row[0]:,}")

  print("  date range: 2001-01-01 - 2021-07-31")

  sql = """Select sum(Num_Riders)
          From Ridership;"""
  dbCursor.execute(sql)
  total = dbCursor.fetchone()
  print("  Total ridership:", f"{total[0]:,}")

  sql = """Select sum(Num_Riders)
          From Ridership
          Where Type_of_Day = 'W';"""
  dbCursor.execute(sql)
  weekday = dbCursor.fetchone()
  weekPercent = weekday[0] / total[0]
  print("  Weekday ridership:", f"{weekday[0]:,}"
    ,"({:.2%})".format(weekPercent))

  sql = """Select sum(Num_Riders)
          From Ridership
          Where Type_of_Day = 'A';"""
  dbCursor.execute(sql)
  sat = dbCursor.fetchone()
  satPercent = sat[0] / total[0]
  print("  Saturday ridership:", f"{sat[0]:,}"
  ,"({:.2%})".format(satPercent))

  sql = """Select sum(Num_Riders)
          From Ridership
          Where Type_of_Day = 'U';"""
  dbCursor.execute(sql)
  sun = dbCursor.fetchone()
  sunPercent = sun[0] / total[0]
  print("  Sunday/holiday ridership:", f"{sun[0]:,}"
  ,"({:.2%})".format(sunPercent))

def command1():          # function for command 1
  dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
  dbCursor = dbConn.cursor()
  print()
  psname = input("Enter partial station name (wildcards _ and %): ")    # getting the input from the user
  sql = """Select Station_ID, Station_Name
          From Stations
          Where Station_Name like ?
          order by Station_Name asc;"""
  dbCursor.execute(sql, [psname])
  cmd1 = dbCursor.fetchall()
  if len(cmd1) == 0:
    print("**No stations found...")
  else: 
    for row in cmd1:
      print(row[0], ':', row[1])

def command2():          # function for command 2
  print("** ridership all stations **")
  dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
  sql = """Select Station_Name, sum(Num_Riders)
          From Ridership join Stations
          on (Ridership.Station_ID = Stations.Station_ID)
          group by Station_Name
          order by Station_Name asc;"""
  sql2 = """Select sum(Num_Riders)
          From Ridership;"""
  dbCursor1 = dbConn.cursor()
  dbCursor1.execute(sql)
  cmd2 = dbCursor1.fetchall()
  dbCursor1.execute(sql2)
  total = dbCursor1.fetchall()
  for x in cmd2:
    cmd2percent = (x[1] / total[0][0]) * 100
    print(x[0], ":", f"{x[1]:,}", f"({cmd2percent:.2f}%)")

def command3():          # function for command 3
  print("** top-10 stations **")
  dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
  sql = """Select Station_Name, sum(Num_Riders)
          From Ridership join Stations
          on (Ridership.Station_ID = Stations.Station_ID)
          group by Station_Name
          order by sum(Num_Riders) desc
          limit 10;"""
  sql2 = """Select sum(Num_Riders)
          From Ridership;"""
  dbCursor1 = dbConn.cursor()
  dbCursor1.execute(sql)
  cmd2 = dbCursor1.fetchall()
  dbCursor1.execute(sql2)
  total = dbCursor1.fetchall()
  for x in cmd2:
    cmd2percent = (x[1] / total[0][0]) * 100
    print(x[0], ":", f"{x[1]:,}", f"({cmd2percent:.2f}%)")

def command4():          # function for command 4
  print("** least-10 stations **")
  dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
  sql = """Select Station_Name, sum(Num_Riders)
          From Ridership join Stations
          on (Ridership.Station_ID = Stations.Station_ID)
          group by Station_Name
          order by sum(Num_Riders) asc
          limit 10;"""
  sql2 = """Select sum(Num_Riders)
          From Ridership;"""
  dbCursor1 = dbConn.cursor()
  dbCursor1.execute(sql)
  cmd2 = dbCursor1.fetchall()
  dbCursor1.execute(sql2)
  total = dbCursor1.fetchall()
  for x in cmd2:
    cmd2percent = (x[1] / total[0][0]) * 100
    print(x[0], ":", f"{x[1]:,}", f"({cmd2percent:.2f}%)")

def command5():          # function for command 5
  dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
  dbCursor = dbConn.cursor()
  print()
  color = input("Enter a line color (e.g. Red or Yellow): ")    # getting the input from the user
  sql = """Select Stop_Name, Direction, ADA
          From Stops
          join Lines
          join StopDetails
          on (Lines.Line_ID = StopDetails.Line_ID and StopDetails.Stop_ID = Stops.Stop_ID)
          Where Color like ?
          order by Stop_Name asc;"""
  dbCursor.execute(sql, [color])
  cmd5 = dbCursor.fetchall()
  if len(cmd5) == 0:
    print("**No such line...")
  else: 
    for row in cmd5:
      if row[2] == 1:
        print(row[0], ':', "direction =", row[1], "(accessible?", "yes)")
      else:
        print(row[0], ':', "direction =", row[1], "(accessible?", "no)")

def command6():          # function for command 6
  print("** ridership by month **")
  dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
  dbCursor = dbConn.cursor()
  sql = """Select strftime('%m', date(Ride_Date)), sum(Num_Riders)
          From Ridership
          Where strftime('%m', date(Ride_Date)) between '01' and '12'
          group by strftime('%m', date(Ride_Date))
          order by strftime('%m', date(Ride_Date)) asc;"""
  dbCursor.execute(sql)
  cmd6 = dbCursor.fetchall()
  for x in cmd6:
    print(x[0], ':', '{:,}'.format(x[1]))
  print()
  plot = input("Plot? (y/n) \n")          # plotting process starts here
  if(plot == 'y'):
    x = []
    y = []
    for row in cmd6:
      x.append(row[0])
      y.append(row[1])
    figure.xlabel("month")
    figure.ylabel("number of riders(x*10^8)")
    figure.title("monthly ridership")
    figure.plot(x, y)
    figure.show()

def command7():          # function for command 7
  print("** ridership by year **")
  dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
  dbCursor = dbConn.cursor()
  sql = """Select strftime('%Y', date(Ride_Date)), sum(Num_Riders)
          From Ridership
          Where strftime('%Y', date(Ride_Date)) between '2001' and '2021'
          group by strftime('%Y', date(Ride_Date))
          order by strftime('%Y', date(Ride_Date)) asc;"""
  dbCursor.execute(sql)
  cmd7 = dbCursor.fetchall()
  for x in cmd7:
    print(x[0], ':', '{:,}'.format(x[1]))
  print()
  plot = input("Plot? (y/n) \n")          # plotting process starts here
  if(plot == 'y'):
    x = []
    y = []
    for row in cmd7:
      x.append(row[0][2:4])
      y.append(row[1])
    figure.xlabel("year")
    figure.ylabel("number of riders(x*10^8)")
    figure.title("yearly ridership")
    figure.plot(x, y)
    figure.show()
    return

def command8():          # function for command 8
  sql = """Select * from Stations
          Where Station_Name like ?;"""
  dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
  dbCursor = dbConn.cursor()
  year = input("\nYear to compare against? ")    # getting the input from the user
  print()
  s1 = input("Enter station 1 (wildcards _ and %): ")    # getting the input from the user
  dbCursor.execute(sql, [s1])
  cmd8 = dbCursor.fetchall()
  if (len(cmd8) == 0):
    print("**No station found...")
    print()
    return
  elif (len(cmd8) > 1):
    print("**Multiple stations found...")
    print()
    return
  print()
  s2 = input("Enter station 2 (wildcards _ and %): ")    # getting the input from the user
  dbCursor.execute(sql, [s2])
  cmd8e = dbCursor.fetchall()
  if (len(cmd8e) == 0):
    print("**No station found...")
    print()
    return
  elif (len(cmd8e) > 1):
    print("**Multiple stations found...")
    print()
    return
  sql2 = """Select date(Ride_Date), Num_Riders
          from Ridership
          where strftime('%Y', Ride_Date) like ?
          and Station_ID like ?
          order by date(Ride_Date) asc;"""
  sql3 = """Select date(Ride_Date), Num_Riders
          from Ridership
          where strftime('%Y', Ride_Date) like ?
          and Station_ID like ?
          order by date(Ride_Date) asc
          limit 5;"""
  sql4 = """Select date(Ride_Date), Num_Riders
          from Ridership
          where strftime('%Y', Ride_Date) like ?
          and Station_ID like ?
          order by date(Ride_Date) desc
          limit 5;"""
  for x in cmd8:
    print("Station 1: ", x[0], x[1])
  dbCursor.execute(sql2, [year, cmd8[0][0]])
  cmd8b = dbCursor.fetchall()
  dbCursor.execute(sql3, [year, cmd8[0][0]])
  cmd8c = dbCursor.fetchall()
  dbCursor.execute(sql4, [year, cmd8[0][0]])
  cmd8d = dbCursor.fetchall()
  for x in cmd8c:
    print(x[0], x[1])
  cmd8d.reverse()
  for x in cmd8d:
    print(x[0], x[1])
  dbCursor.execute(sql, [s2])
  cmd8a = dbCursor.fetchall()
  for x in cmd8a:
    print("Station 2: ", x[0], x[1])
  dbCursor.execute(sql3, [year, cmd8e[0][0]])
  cmd8f = dbCursor.fetchall()
  dbCursor.execute(sql4, [year, cmd8e[0][0]])
  cmd8g = dbCursor.fetchall()
  for x in cmd8f:
    print(x[0], x[1])
  cmd8g.reverse()
  for x in cmd8g:
    print(x[0], x[1])
  print()
  plot = input("Plot? (y/n) \n")          # plotting process starts here
  if(plot == 'y'):
    x = []
    y = []
    for row in cmd8:
      x.append(row[0])
      y.append(row[1])
    figure.title(" riders each day of " + year)
    figure.plot(x[0], cmd8b[1][1])
    figure.plot(x[0], cmd8e[0][0])
    figure.show()

def command9():          # function for command 9
  dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
  dbCursor = dbConn.cursor()
  color = input("\nEnter a line color (e.g. Red or Yellow): ")    # getting the input from the user
  sql = """Select Station_Name, Latitude, Longitude
          From Stations
          join Lines
          join Stops
          join StopDetails
          on (Lines.Line_ID = StopDetails.Line_ID and StopDetails.Stop_ID = Stops.Stop_ID and Stops.Station_ID = Stations.Station_ID)
          Where Color like ?
          group by Station_Name
          order by Station_Name asc;"""
  dbCursor.execute(sql, [color])
  cmd9 = dbCursor.fetchall()
  if len(cmd9) == 0:
    print("**No such line...")
    return
  else: 
    for row in cmd9:
      print(row[0], ':', "({},".format(row[1]), 
      "{})".format(row[2]))
  print()
  plot = input("Plot? (y/n) \n")          # plotting process starts here
  if(plot == 'y'):
    x = []
    y = []
    for row in cmd9:
      x.append(row[2])
      y.append(row[1])
    image = figure.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
    figure.imshow(image, extent=xydims)
    figure.title(color + " line ")
    if(color.lower() == "purple-express"):
      color = "Purple"
    figure.plot(x, y, "o", c=color)
    for row in cmd9:
      figure.annotate(row[0], (row[2], row[1]))
    figure.xlim([-87.9277, -87.5569])
    figure.ylim([41.7012, 42.0868])
    figure.show()

printstats()

print()

while (True):        # loop to allow user to use the program as long as he needs
  cmd = input("Please enter a command (1-9, x to exit): ")     # getting the command from the user
  if(cmd == '1'):
    command1()
  elif(cmd == '2'):
    command2()
  elif(cmd == '3'):
    command3()
  elif(cmd == '4'):
    command4()
  elif(cmd == '5'):
    command5()
  elif(cmd == '6'):
    command6()
  elif(cmd == '7'):
    command7()
  elif(cmd == '8'):
    command8();
  elif(cmd == '9'):
    command9()
  elif(cmd == 'x'):       # if the user wants to exit, then breaking out of loop
    break
  else:
    print("**Error, unknown command, try again...")
    print()
  

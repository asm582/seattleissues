"""
<Program Name>
  geoip_response.py

<Purpose>
  This is a monitoring script to test how many times the geoip server is
  failing to respond in a given amount of time. It will send an email if
  an server did not respond.

<Side Effects>
  Creates a file named geoip_failuer_test.out, to log all the valid responses. 
"""
import repyhelper
import time
import integrationtestlib

repyhelper.translate_and_import('poll_geoservers.r2py')
TEST_IP =[]
TEST_IP = ['128.238.63.50','128.238.63.15']
def sendmail(start_time, err_msg, elapsed_time, err_interval, counter,IP):
  # Recipient email to the send the notification...
  integrationtestlib.notify_list = ['asm582@nyu.edu']

  subject = "Error caught while testing GeoIP."
  
  message = "Monitoring script started at: " + str(time.ctime(start_time))
  message += "\n Error occurred " + str(counter) + " times, in the last " +\
   str(elapsed_time/60.0) + " mins."
  message += "\n Time since the last error: " + str(err_interval/60.0)
  message += "\n Error: "+ str(err_msg) + "\n\n"

  integrationtestlib.notify(message, subject)


def main():
  # Save the time when the script started to monitor...
  start_time = time.time()


  # Keep a tab on how many times the geoip server is failing to respond. 
  counter = 0
  err_time = 0.0

  # Run the script for 18 hours and then quit...
  while (time.time() - start_time) <= (18*60*60):
    try:
      # Query the location of an IP and check whether the server is failing
      # to respond or not...
      for IP in TEST_IP:
        ret = poll(IP)
        if(str(ret) == "Timed-out connecting to the remote host!" or str(ret) == "Cannot bind to the specified local ip, invalid!"):  
          counter += 1
          ret = str(IP)+":"+ret
          prev_err_time = err_time
          err_time = time.time()
          sendmail(start_time, ret, err_time - start_time,
          err_time - prev_err_time, counter, IP)
          print "a mail was sent"
      # log the successful results into a file...
        else:
          ret = str(IP)+":"+ret
          open("geoip_failure_test.out", "a").write(str(err_time)+" "+ str(ret) + '\n')
        ret = ""
    except Exception, err:
     
      #if anyother error exists the thi triggers mail
      err = str(err)
      prev_err_time = err_time
      err_time = time.time()
      sendmail(start_time, err, err_time - start_time,
        err_time - prev_err_time, counter)
      print "a mail was sent"
      
    finally:
      # whatever the result is, wait for 15 mins and retry...
      time.sleep(15*60)

if __name__ == '__main__':
  main() 

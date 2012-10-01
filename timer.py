"""
Simple timing class. Shamelessly stolen from
http://mrooney.blogspot.com/2009/07/simple-timing-of-python-code.html
"""
import time

class Timer():
   def __enter__(self): self.start = time.time()
   def __exit__(self, *args): print "Execution time: ", time.time() - self.start

# PROJECT COGSWORTH
## An attempt at seeing what would happen if a pidgeon #@!$#@ a wifi chipset.

**What_Does_The_Scouter_Say_About_His_Power_Level.grc** The GNU Radio program that reads off the HackRF connected to the antenna we wiggle around with robotic (handcut) precision. Outputs the signal power level onto the network as UDP packets stuffed with a chewy little endian 32 bit float center. Spared no expense! (Nervously checks for raptors...)  
  
**manip.py** Nothing fancy aside from it uses ALL THE DATA you've collected. But it's parallelized...so the more cores, the faster. So at least is has that going for it. You may have to up your allowed open file descriptor with `ulimit -n 65000`. Solid State Drives are nice for this part as well...  
  
**wiggle.py** Contains the code that generates the GCODE used to control the robotic component, as well as feeding that generated command stream to the robot itself. It also runs a thread that samples for 250ms off of a UDP port set to 9000. It writes these to individual files for each sample.  
  
The controller is an AVR development board (also known by lesser mortals as an Arduino...) with a RAMPS1.4 daughterboard (outside of engineering circles, also known as a shield...).  
It drives a pair of unipolar steppers with a step resolution of about 200 full steps per revolution.  
  
It's recommended you figure out how to at least run this on PyPy to have human-scale processing times.  
  
For the rest of you, I leave getting this to compile to LLVM-IR as an exercise to the reader...  
  
To go with the following video series...  
  
Part 1 => https://www.youtube.com/watch?v=o6WHhqDHSQ4  
Part 2 => https://www.youtube.com/watch?v=VABeN4uv03s  

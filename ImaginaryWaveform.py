import pygame
import pyaudio
import numpy as np
import time
import wave
import scipy.fftpack
from functools import lru_cache

from video import make_video
pygame.init()   

surface_size = 1000
main_surface = pygame.display.set_mode((1000,1000),pygame.DOUBLEBUF)
my_clock = pygame.time.Clock()

lru_cache(maxsize=None)
def draw_tree(inord, order, theta, thetab, sz, posn, heading, color=(0,0,0), depth=0):

   trunk_ratio = (1 + 5 ** 0.5) / 2       
   trunk = sz * trunk_ratio
   delta_y = trunk * np.sin((heading*400/400).real)
   delta_x = trunk * np.cos((heading*400/400).real)

   thetaj = theta*1j*1j
   thetai = thetab*1j*1j
   
   (u, v) = posn
   newpos = (u + delta_x, v + delta_y)
   #Draw final end
   #if order==1:
   
   #Draw all 
   if True:
      pygame.draw.line(main_surface, color, newpos, newpos, 1)
   
   gradd  = 128+(127*(np.cos((heading*1j).imag)))
   gradd2 = 128+(127*(np.sin((heading).real)))
   gradd3 = 128+(128*np.sin((heading*1j).imag))
   gradd4 = 128+(128*np.cos((heading).real))
   gradd5 = 128+(128*np.sin((heading).real))
   gradd6 = 128+(128*np.sin((heading).real))
   

   if order > 0:
      color1 = (gradd,gradd2,gradd3)
      color2 = (gradd,gradd2,gradd3)

      newsz = sz*(1 - trunk_ratio)
      draw_tree(inord, order-1, theta, thetab, newsz, newpos, (heading+theta+12j), color1, depth)
      draw_tree(inord, order-1, theta, thetab, newsz, newpos, (heading+thetab+12j), color2, depth)
      

def gameloop():
    theta1 = 0
    theta2 = 0
    frame = 0
    inord = 0
    headingin = 0
   
    WIDTH = 4
    CHANNELS = 1
    RATE = 22050

    save_screen = make_video(main_surface)
    
    wf = wave.open('long.wav', 'rb')
    song = wave.open('10simm.wav', 'rb')
    p = pyaudio.PyAudio()

    main_surface.fill((0, 0, 0))
    
   
    def callback(in_data, frame_count, time_info, status):
       #Uncomment to output frames
       #next(save_screen)
       data = wf.readframes(frame_count)
       data2 = song.readframes(frame_count)
       
       decoded = np.fromstring(data, dtype=np.int32)
       decoded2 = np.fromstring(data2, dtype=np.int32)
       
       if np.fabs(decoded[0]) > 0:
           if np.fabs(decoded[1]) > 0:
               for i,l in zip(decoded,decoded2):
                  
                  theta1 = (2*np.pi*(i/2147483647))
                  theta2 = np.cos(2*np.pi*(np.exp((l/50)/2147483647)))+np.sin(-2*np.pi*(np.exp((l/50)/2147483647)))

                  draw_tree(inord,2, theta1, theta2, surface_size*0.3*(i/2147483647), (500,500), (i/2147483647)*np.pi*(np.exp((l/50)/2147483647)))

       return (data, pyaudio.paContinue)
      
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=96000,
                output=True,
                stream_callback=callback)
    stream.start_stream()
    
    while True:
        pygame.display.flip()
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break;
         #Output current screen 
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_s:
           next(save_screen)

gameloop()
pygame.quit()

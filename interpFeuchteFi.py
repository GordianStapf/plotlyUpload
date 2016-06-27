# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 16:49:28 2016

@author: stapfg
"""

def widerstand2Feuchte_Fi(r):
    from numpy import array, interp, nan
    
    R = array([43.4, 45.1, 46.7, 47.6, 48.3, 49.1, 49.9, 51.8, 53.4, 55.1,56.7,	
                  57.4, 58.2, 60.0, 70.1, 80.0, 90.0, 100.0, 103.0, 110.0])
    
    U = array([77.0, 68.1, 60.2, 56.0, 52.6, 48.2, 45.4, 38.5, 33.8, 29.8, 27.1,
                  25.9, 24.9, 23.0, 17.6, 14.5, 11.7, 8.9, 8.0, 6.2,])
                  
    u = interp(r, R, U, left=nan, right=nan)
    
    return u
    
def tempKompFeuchte(u,t):
    u_korr = u+((0.2665*u+2.8148)/15.8)*(
                -0.00001*t**3+0.003*t**2-0.4905*t+10.517)
    return u_korr
    
def widerstand2feuchteFi_t_komp(r,t):
    u = widerstand2Feuchte_Fi(r)
    u_korr = tempKompFeuchte(u,t)
    return u_korr

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import scipy
import datetime
from matrices import Matrices


def profit(X,prices) : 
        return sum([vol * price for vol,price in zip(X,prices)])

class Optimizer :
    def __init__(self,stockage):
        self.prices = stockage.data['Price']
        self.stock = stockage
        self.m = stockage.m
        self.initial_vect  = self.stock.Vinit * np.ones((self.stock.N))
        self.X_0 = np.zeros(self.stock.N,)
    
       
    def con_max_sout(self,x):
        return  - ( self.stock.sout_corrige(x)- x)

    def con_max_inj(self,x):
        return self.stock.inj_corrige(x) - x

    def con_inf(self,x):
        V = self.stock.Vmax*np.dot(self.stock.m.triang_inf,x) + self.stock.Vinit*np.ones(self.stock.N)
        return  V - self.stock.lim_min

    def con_sup(self,x):
        V = self.stock.Vmax*np.dot(self.stock.m.triang_inf,x) + self.stock.Vinit*np.ones(self.stock.N)
        return  self.stock.lim_max - V

    def contraints_init(self):
        #Positivité des échanges
        
        self.c1 = scipy.optimize.LinearConstraint(np.eye(self.stock.N),-1,1)
        self.c3 = scipy.optimize.LinearConstraint(self.stock.Vmax*self.m.triang_inf,
                                                self.stock.vect_min - self.initial_vect, 
                                                self.stock.vect_max - self.initial_vect)
        self.c4 = scipy.optimize.NonlinearConstraint(lambda x : self.con_max_sout(x),0, np.inf)
        self.c5 = scipy.optimize.NonlinearConstraint(lambda x : self.con_max_inj(x),0, np.inf)
        self.c6 = scipy.optimize.NonlinearConstraint(lambda x : self.con_inf(x),0, np.inf)
        self.c7 = scipy.optimize.NonlinearConstraint(lambda x : self.con_sup(x),0, np.inf)

    def optimize(self):
        res = minimize(lambda x:profit(x, self.prices), self.X_0 ,method='SLSQP', constraints = [self.c1,self.c4,self.c5, self.c6, self.c7], options={'disp' : True, 'ftol': 1e-1})
        self.stock.evolution = res.x

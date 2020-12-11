# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Kalman filter class
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import misc.params as params 

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        pass

    def F(self):
        ############
        # TODO Step 1: implement and return system matrix F
        ############
        dt = params.dt
        n = params.dim_state
        F = np.identity(params.dim_state).reshape(n,n)
        F[0, 3] = dt 
        F[1, 4] = dt 
        F[2, 5] = dt 

        return np.matrix(F)
        
        ############
        # END student code
        ############ 

    def Q(self):
        ############
        # TODO Step 1: implement and return process noise covariance Q
        ############
        dt = params.dt
        Q = np.zeros((params.dim_state, params.dim_state))
        np.fill_diagonal(Q, dt* params.q)

        return np.matrix(Q)
        
        ############
        # END student code
        ############ 

    def predict(self, track):
        ############
        # TODO Step 1: predict state x and estimation error covariance P to next timestep, save x and P in track
        ############
        F = self.F()
        Q = self.Q()
        x = F * track.x 
        P = F * track.P * F.T + Q
        
        track.set_x(x)
        track.set_P(P)
        
        
        ############
        # END student code
        ############ 

    def update(self, track, meas):
        ############
        # TODO Step 1: update state x and covariance P with associated measurement, save x and P in track
        ############
        
        x = track.x
        P = track.P 
        
        y = self.gamma(track, meas)
        H = meas.sensor.get_H(x)
        S = self.S(track, meas, H)
        
        K = P * H.T * S.I 
        I = np.identity(params.dim_state)
        
        x = x + K*y
        P = (I - K * H) * P
        
        track.set_x(x)
        track.set_P(P)
        
        ############
        # END student code
        ############ 
        track.update_attributes(meas)
    
    def gamma(self, track, meas):
        ############
        # TODO Step 1: calculate and return residual gamma
        ############
        z = meas.z
        z_pred = meas.sensor.get_hx(track.x)
        y = z - z_pred

        return y
        
        ############
        # END student code
        ############ 

    def S(self, track, meas, H):
        ############
        # TODO Step 1: calculate and return covariance of residual S
        ############
        
        S = H * track.P * H.T + meas.R
        

        return S
        
        ############
        # END student code
        ############ 
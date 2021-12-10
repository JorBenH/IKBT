#!/usr/bin/python
#
#     Classes to generate LaTex outputs
#

# Copyright 2017 University of Washington

# Developed by Dianmu Zhang and Blake Hannaford
# BioRobotics Lab, University of Washington

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import sympy as sp
import shutil as sh
import os as os
#import numpy as np
import ikbtbasics.pykinsym as pks
import re
from ikbtbasics.solution_graph_v2 import *
import ikbtbasics.matching as mtch
import sys as sys
import b3 as b3          # behavior trees
import pickle
from ikbtfunctions.helperfunctions import *
import ikbtfunctions.graph2latex as gl
#from kin_cl import *
import ikbtbasics.kin_cl as kc


class LatexFile(fname):
    def __init__():
        self.filename = fname + '.tex'
        if self.filename.endswith('.tex.tex'):
            self.filename = self.filename[:-4]
        print('Working with Latex file: ',self.filename)
        self.preamble = [] # list of line strings
        self.sections = [] # list of lists of line strings
        self.close =    []  # list of line strings
        
        f = open('IKBT/IK_preamble.tex','r')
        self.preamble = f.readlines()
        f.close()
        f = open('IKBT/IK_close.tex','r')
        self.close = f.readlines()
        f.close()
        
    def set_title(title):        
        self.preamble.append['\n']
        self.preamble.append('\begin{center} \section*{***TITLE***} \end{center}\n'.replace(title)]

        
    #  optional to override the template file in /LaTex
    def set_preamble(str):
        self.preamble = str;
        
        
    #  output the final latex file
    def output():
        f = open(self.filename,'w') 
        plines(self.preamble,f)
        for s in self.sections:
            print('\n\n')
            plines(s,f)
        plines(self.close,f)
        f.close()
        

def plines(sl,f):
    for s in sl:
        print(s, file=f)
    
# convert a big string with \n's into a list of strings
def breaklines(s):
    

#
#      Generate a complete report in latex
#
def output_latex_solution(Robot,variables, groups):
    GRAPH = True
    ''' Print out a latex document of the solution equations. '''

    orig_name =  Robot.name.replace('test: ','')
    fixed_name = orig_name.replace(r'_', r'\_')

    DirName = 'LaTex/'
    defaultname = DirName + 'IK_solution.tex'
    fname = DirName + 'IK_solution_'+orig_name+'.tex'
    LF = LatexFile(fname)
    
    ####################   Intro Section
    
    introstring = r'''
    \begin{center}
    \section*{Inverse Kinematic Solution for ''' + fixed_name + r'''}
    \today
    \end{center}
    \section{Introduction}
    This report describes closed form inverse kinematics solutions for '''+fixed_name+r'''.
    The solution was automatically generated by the IK-BT package from the University of Washington Biorobotics Lab.
    The IK-BT package is described in
    \url{https://arxiv.org/abs/1711.05412}.  IK-BT derives your inverse kinematics equations
    using {\tt Python 2.7} and the {\tt sympy} module for symbolic mathematics.
    '''
    
    LF.sections.append(introstring.splitlines())
    
    ####################   Kinematic params
    
    paramsection = r'''\section{Kinematic Parameters}
    The kinematic parameters for this robot are
    \[ \left [ \alpha_{i-1}, \quad a_{i-1}, \quad d_i, \quad \theta_i \right  ] \]
    \begin{dmath}''' + sp.latex(Robot.Mech.DH) +  r'\end{dmath}'
    
    LF.sections.append(paramsection.splitlines())
    
    ####################  Forward Kinematics
    
    

    fksection = r'''\section{Forward Kinematic Equations}
    The forward kinematic equations for this robot are:''',file=f)


    LHS = ik_lhs()
    RHS = kc.notation_squeeze(Robot.Mech.T_06)   # see kin_cl.mechanism.T_06
    print(r'\begin{dmath}', file=f)
    print(sp.latex(LHS) + r' =  \\', file=f)
    COLUMNS = True
    if COLUMNS:
        for c in range(4):
            print(r'\mathrm{'+'Column  {:}'.format(c)+r'}', file=f)
            print(sp.latex(RHS[:,c]),file=f)
            print(r'\\',file=f)
    else:
        print(sp.latex(RHS), file=f)
    print(r'\end{dmath}', file=f)

    
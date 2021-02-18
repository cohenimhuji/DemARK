# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: collapsed
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.1
#   kernel_info:
#     name: python3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # The Tractable Buffer Stock Model

# %% {"code_folding": [0]}
# This cell has just a bit of initial setup. You can click the arrow to expand it.
# %matplotlib inline
import matplotlib.pyplot as plt

import sys 
import os
sys.path.insert(0, os.path.abspath('../lib'))

import numpy as np
import HARK 
from time import clock
from copy import deepcopy
mystr = lambda number : "{:.3f}".format(number)

from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

from HARK.utilities import plotFuncs
from HARK.ConsumptionSaving.TractableBufferStockModel import TractableConsumerType

# %% [markdown]
# The [TractableBufferStock](http://www.econ2.jhu.edu/people/ccarroll/public/LectureNotes/Consumption/TractableBufferStock/) model is a (relatively) simple framework that captures all of the qualitative, and many of the quantitative features of optimal consumption in the presence of labor income uncertainty.  
#
# The key assumption behind the model's tractability is that there is only a single, stark form of uncertainty.  So long as an employed consumer remains employed, his labor income will rise at a constant rate.  But between any period and the next there is constant hazard $p$ of transitioning to the "unemployed" state. Unemployment is irreversible, like retirement or disability.  When unemployed, the consumer receives a fixed amount of income (for simplicity, zero).
#
# \begin{eqnarray*}
# \mathbb{E}_{t}[V_{t+1}^{\bullet}(M_{t+1})] & = & (1-p)V_{t+1}^{e}(M_{t+1})+p V_{t+1}^{u}(M_{t+1})
# \end{eqnarray*}
#
# A consumer with CRRA utility $U(C) = \frac{C^{1-\rho}}{1-\rho}$ solves an optimization problem that looks standard (where $P$ is Permanent income and $\Gamma$ is the income growth factor):
#
# \begin{eqnarray*}
# V_t(M_t) &=& \max_{C_t} ~ U(C_t) + \beta \mathbb{E}[V_{t+1}^{\bullet}], \\
# M_{t+1} &=& R A_t + \mathbb{1}(P_{t+1}), \\
# P_{t+1} &=& \Gamma_{t+1} P_t,
# \end{eqnarray*}
#
# where $\mathbb{1}$ is an indicator of whether the consumer is employed in the next period.
#
# Under plausible parameter values the model has a target level of $m = M/P$ (market resources to permanent income) with an analytical solution that exhibits plausible relationships among all of the parameters.  (See the linked handout for details).

# %% {"code_folding": []}
# Define a parameter dictionary and representation of the agents for the tractable buffer stock model
TBS_dictionary =  {'UnempPrb' : .00625,    # Probability of becoming unemployed
                   'DiscFac' : 0.975,      # Intertemporal discount factor
                   'Rfree' : 1.01,         # Risk-free interest factor on assets
                   'PermGroFac' : 1.0025,  # Permanent income growth factor (uncompensated)
                   'CRRA' : 1.5}           # Coefficient of relative risk aversion
MyTBStype = TractableConsumerType(**TBS_dictionary)

# %% [markdown]
# ## Target Wealth
#
# Whether the model exhibits a "target" or "stable" level of wealth for employed consumers depends on whether the 'Growth Impatience Condition' (the GIC) holds:
#
# \begin{equation}\label{eq:GIC}
#  \left(\frac{(R \beta (1-\mho))^{1/\rho}}{\Gamma}\right)  <  1
# \end{equation}
#

# %% [markdown]
# ### IMPORTENT: To activate: jupyter-js-widgets/extension in the nbextensions

# %% {"code_folding": []}
# Make an interactive plot of the tractable buffer stock solution

# To make some of the widgets not appear, replace X_widget with fixed(desired_fixed_value) in the arguments below.
interact(makeTBSplot,
         DiscFac = DiscFac_widget,
#         CRRA = CRRA_widget,
         CRRA = fixed(2.5),
         Rfree = Rfree_widget,
         PermGroFac = PermGroFac_widget,
         UnempPrb = UnempPrb_widget,
         mMin = mMin_widget,
         mMax = mMax_widget,
         cMin = cMin_widget,
         cMax = cMax_widget,
         show_targ = show_targ_widget,
         plot_emp = plot_emp_widget,
         plot_ret = plot_ret_widget,
         plot_mSS = plot_mSS_widget,
        );


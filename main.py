# Import functions from data_cleanup.py
from data_utils import *
from graph_utils import *

data = initialize()
display(data)
display(data.groupby('year')['nb_actes'].sum().reset_index())

plot_global_acte_per_year(data)
plot_stacked_acte_per_year(data)
plot_actes(data)
plot_actes_per_year(data)
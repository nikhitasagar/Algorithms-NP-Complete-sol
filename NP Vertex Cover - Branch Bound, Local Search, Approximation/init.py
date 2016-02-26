from ApproxFinal import Approx_Final
from FinalBnBNikhita import BnB_Final
from tempBnB import BnB_Final2
from tempBnBAlternate import BnB_Final3

def initialize_project(filename, cutoff, method_use, random_seed):
    if method_use == "Approx":
        Approx_Final(filename, cutoff)
    elif method_use == "BnB":
        BnB_Final3(filename, cutoff, random_seed)

    #elif method_use == "LS":


initialize_project("netscience", 60*10, "BnB", 0)


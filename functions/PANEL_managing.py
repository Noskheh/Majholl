#this is functions that managing panels

#- output panel pk
def getting_panel_pk(panel_pk):
    zero_value = '0'
    for keys , values in panel_pk.items():
        if values != 0 :
            return str(values)
        else :
            return zero_value
        



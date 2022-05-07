#DICTIONARY OF LAYOUT FUNCTIONS FOR PORTFOLIO GENERATOR 
# from dash import dash_table, dcc, html
import dash_bootstrap_components as dbc


def ps5_skeleton(cards):
    layoutChild = [
        dbc.Row([
            dbc.Col([cards[0]],width=3), dbc.Col([cards[1]],width=3), dbc.Col([cards[2]],width=3)#, dbc.Col([cards[0]],width=3),
        ]),
        dbc.Row([
            dbc.Col([cards[3]],width="auto"), dbc.Col([cards[4]],width="auto")#, dbc.Col([cards[0]])
        ])]
    return layoutChild
        
def ps6_skeleton(cards):
    layoutChild = [
        dbc.Row([
            dbc.Col([cards[0]],width=3), dbc.Col([cards[1]],width=3), dbc.Col([cards[2]],width=3)#, dbc.Col([cards[0]],width=3),
        ]),
        dbc.Row([
            dbc.Col([cards[3]],width="auto"), dbc.Col([cards[4]],width="auto"),dbc.Col([cards[5]],width="auto")
        ])]
    return layoutChild

def ps7_skeleton(cards):
    layoutChild = [
        dbc.Row([
            dbc.Col([cards[0]],width=3), dbc.Col([cards[1]],width=3), dbc.Col([cards[2]],width=3),dbc.Col([cards[3]],width="auto")
        ]),
        dbc.Row([
            dbc.Col([cards[4]],width="auto"),dbc.Col([cards[5]],width="auto"),dbc.Col([cards[6]],width="auto")
        ])]        
    return layoutChild
  
def ps8_skeleton(cards):
    layoutChild = [
        dbc.Row([
            dbc.Col([cards[0]],width=3), dbc.Col([cards[1]],width=3), dbc.Col([cards[2]],width=3),dbc.Col([cards[3]],width="auto")
        ]),
        dbc.Row([
            dbc.Col([cards[4]],width="auto"),dbc.Col([cards[5]],width="auto"),dbc.Col([cards[6]],width="auto"), dbc.Col([cards[7]],width="auto")
        ])]        
    return layoutChild

def ps9_skeleton(cards):
    layoutChild = [
        dbc.Row([
            dbc.Col([cards[0]],width=3), dbc.Col([cards[1]],width=3), dbc.Col([cards[2]],width=3)#, dbc.Col([cards[0]],width=3),
        ]),
        dbc.Row([
            dbc.Col([cards[3]],width="auto"), dbc.Col([cards[4]],width="auto"),dbc.Col([cards[5]],width="auto")
        ]),
        dbc.Row([
            dbc.Col([cards[6]],width="auto"), dbc.Col([cards[7]],width="auto"),dbc.Col([cards[8]],width="auto")
        ])]
    return layoutChild

def ps10_skeleton(cards):
    layoutChild = [
        dbc.Row([
            dbc.Col([cards[0]],width=3), dbc.Col([cards[1]],width=3), dbc.Col([cards[2]],width=3),dbc.Col([cards[3]],width="auto")
        ]),
        dbc.Row([
            dbc.Col([cards[4]],width="auto"),dbc.Col([cards[5]],width="auto"),dbc.Col([cards[6]],width="auto"), dbc.Col([cards[7]],width="auto")
        ]), 
        dbc.Row([
            dbc.Col([cards[8]],width="auto"), dbc.Col([cards[9]],width="auto")
        ])]
    return layoutChild


layout_dict = {
                5:ps5_skeleton,
                6:ps6_skeleton,
                7:ps7_skeleton,
                8:ps8_skeleton,
                9:ps9_skeleton,
                10:ps10_skeleton
               }    
    
    
    

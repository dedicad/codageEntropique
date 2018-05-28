from math import *

def entropie(tab_proba):
    '''Cette fonction calcule l'entropie du tableau de probabilité fourni en entrée sous la forme de tuple (frequence, motif)'''
    somme = 0
    for (pi,elm) in tab_proba:
        somme += pi*log(pi,2)
    return -somme
    

def recup(liste,elm):
    '''Cette fonction permet de récupérer l'indice de l'élément (*,elm) dans la liste de tuple liste'''
    for i in range(len(liste)):
        if liste[i][1] == elm: return i
    return "L'élément n'est pas présent dans la liste"
    
def longueur_moyenne(source,codage):
    '''Cette fonction calcule la longueur moyenne d'un codage. Elle prend en entrée une liste de tuple (frequence,motif) et une autre liste de tuple (code, motif).'''
    long = 0
    for (freq,motif) in source:
        for (code,motifBis) in codage :
            if motif==motifBis :
                long += len(code)*freq
    return long
    
def Huffman(tab_proba):
    """Cette fonction prend en entrée une liste de tuple (frequence,motif)
    et retourne une liste de tuple (code, motif)"""
    m = len(tab_proba)
    C = [("0","Initial")]*m                                                                #C est le tableau de tuple que l'on renverra, il est composé de (code, motifACoder)
    if m == 2 :                                                                            #Cas de base de notre algorithme récursif
        C[0],C[1] = ("0",tab_proba[0][1]),("1",tab_proba[1][1])
    else :
        tab_proba.sort(reverse = True)                                                     #On trie la liste des proba dans le sens décroissant
        temp = Huffman(tab_proba[0:-2] + [(tab_proba[-2][0]+tab_proba[-1][0],"new")])      #On applique le procédé sur une liste de taille m-1
        indice = recup(temp,"new")                                                         #On regarde où l'élément "spécial" s'est positionné suite au tri
        temp.append(temp[indice])
        temp.pop(indice)                                                                    #On l'enlève pour le repositionner à la fin de la liste
        for i in range(m-2):                                                                #On récupère les codes pour les m-2 premiers motifs
            C[i] = temp[i]
        C[m-2] = (temp[-1][0]+"0",tab_proba[-2][1])                                         #On crée les codes pour les 2 derniers motifs
        C[m-1] = (temp[-1][0] + "1",tab_proba[-1][1])
    return C
    
test_tab = [(0.05,"a"),(0.9,"b"),(0.05,"c")]
#print (Huffman(test_tab))
    
    
#Source sans mémoire 3-extension
tableau = [(0.729,"000"),(0.081,"001"),(0.081,"010"),(0.009,"011"),(0.081,"100"),(0.009,"101"),(0.009,"110"),(0.001,"111")]
sol = Huffman(tableau)
#print (sol)
#print ("entropie : ",entropie(tableau))
#print ("Longueur moyenne de notre codage :",longueur_moyenne(tableau,sol))

















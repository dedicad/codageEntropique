chemin = "C:/Users\Dedicad\Documents\Centrale-Supélec\Cours\Projet synthèse, codage entropique\Code\codageEntropique/"
import sys 
sys.path.append(chemin)
from CodageHuffmanAvecTuple import *


def code(texte):
    '''Cette fonction prend en entrée un texte sous forme de string, calcule la fréquence d'apparition de chaque symbole,
    et retourne en sortie le code de Huffman obtenu ainsi que le texte codé'''
    n = len(texte)
    if n<2 : return ('Le texte est court')
    else :
        dico = {}
        for lettre in texte:
            if lettre not in dico :
                dico[lettre] = 1
            else : dico[lettre] += 1
        tab = []
        for cle in dico.keys():
            tab.append((dico[cle]/n,cle))
        sol = Huffman(tab)
        #On recrée un dictionnaire parce que c'est plus facile à utiliser
        dico_code = {}
        for (code,motif) in sol:
            dico[motif] = code
        res = ""
        for lettre in texte:
            res += dico[lettre]
        return (res,sol)
        
def decode(texte,codage):
    '''Cette fonction prend en entrée un texte crypté par Huffman et le codage de Huffman associé. 
    Elle retourne le texte décodé'''
    #On crée un dico dont la clé est le code et la valeur le motif associé, parce que c'est plus facile à utilisesr
    dico = {}
    for (code,motif) in codage:
        dico[code] = motif
    res = ""
    i = 0
    while i <len(texte):
        j = i+1
        section =  texte[i:j]
        while section not in dico :
            j += 1
            section =  texte[i:j]
        res += dico[section]
        texte = texte[j:]
    return res

test = code('andrés garçia')
#print (test[0])
#print ("Decodage en cours")
#print ("Le texte décodé : ",decode(test[0],test[1]))

import marshal
#Module pour stocker des listes dans un fichier txt 


def code_fichier(fichier_clair,fichier_crypte,fichier_codage):
    '''Cette fonction prend en entrée le nom d'un fichier texte à crypte et les noms des fichiers où on stockera les sorties et retourne en sortie le code de Huffman obtenu
     ainsi que le texte codé dans le fichier fichier_crypte, qu'elle crée s'il n'existe pas'''
    fichier = open(chemin+fichier_clair,'r') 
    contenu = fichier.read()
    fichier.close()
    temp = code(contenu)
    fichier = open(chemin+fichier_crypte,'w')
    fichier.write(temp[0])
    fichier.close()
    fichier = open(chemin+fichier_crypte,'w')
    fichier.write(temp[0])
    fichier.close()
    marshal.dump(temp[1], open(chemin+fichier_codage,"wb"))
    print ("Le codage a bien été effectué") 

test2 = code_fichier('texte.txt','crypte.txt','codeHuffman.txt')

def decode_fichier(fichier_codage,fichier_crypte,fichier_cible):
    '''Cette fonction prend en entrée un fichier contenant le texte crypté, un autre fichier contenant le codage de Huffman associé, et le fichier où on écrira le texte en clair'''
    fichier = open(chemin+fichier_crypte,'r') 
    contenu = fichier.read()
    fichier.close()
    res = decode (contenu,marshal.load(open(chemin+fichier_codage,"rb")))
    fichier = open(chemin+fichier_cible,'w') 
    fichier.write(res)
    fichier.close()
    print ("Le fichier a été décodé")

test3 = decode_fichier('codeHuffman.txt','crypte.txt','texte_decode.txt')





chemin = "C:/Users\Dedicad\Documents\Centrale-Supélec\Cours\Projet synthèse, codage entropique\Code\codageEntropique/"                              #Emplacement du dossier courant
import sys 
sys.path.append(chemin)
from time import *
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
    tps = time()
    n = len(texte)
    while len(texte)>0:
        j = 1
        section =  texte[0:j]
        while section not in dico :
            j += 1
            section =  texte[0:j]
        res += dico[section]
        texte = texte[j:]
        #Les lignes qui suivent permettent de suivre l'avancement de la fonctions
        if time()-tps > 10:
            print ("On avance")
            tps = time()
        if len(texte)%((n//100+1)*2) ==0 :
            print ("Il reste ",len(texte)//(n//100+1),"% du texte à décoder.")
    return res

test = code('andrés garçia')
#print (test[0])
#print ("Decodage en cours")
#print ("Le texte décodé : ",decode(test[0],test[1]))

#########################################
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

#test2 = code_fichier('texte.txt','crypte.txt','codeHuffman.txt')

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

#test3 = decode_fichier('codeHuffman.txt','crypte.txt','texte_decode.txt')

#########################################

from PIL import Image                                           # On import le module concu pour la manipulation d'image
def code_image(image,fichier_codage,fichier_crypte):
    '''Cette fonction prend en paramètre une image à coder et un fichier où enregistrer le codage de Huffman associé et le fichier où sera stocké l'image crypté sous forme binaire'''
    im = Image.open(chemin+image)
    liste = (list(im.getdata()))
    #Ici on va aplatir la liste et la convertir en une chaine de caractère
    contenu = str(im.size[0])+";"+str(im.size[1])+";"
    for pixel in liste : 
        contenu += str(pixel)+";"
    #Le ; sert de séparateur, comme dans les fichiers csv
    temp = code(contenu)
    fichier = open(chemin+fichier_crypte,'w')
    fichier.write(temp[0])
    fichier.close()
    fichier = open(chemin+fichier_crypte,'w')
    fichier.write(temp[0])
    fichier.close()
    marshal.dump(temp[1], open(chemin+fichier_codage,"wb"))
    print ("Le codage a bien été effectué") 

code_image("image.bmp","codage_image.txt","image_crypte.txt")

def decode_image(image_crypte,fichier_codage,fichier_cible):
    fichier = open(chemin+image_crypte,'r') 
    temp = fichier.read()
    fichier.close()
    res = decode (temp,marshal.load(open(chemin+fichier_codage,"rb")))
    #1e étape : on détermine les données de taille de l'image
    long_temp = []
    i = 0
    for m in range(2):
        j = i+1
        section = res[i:j]
        while res[j] != ';':
            j += 1
        section = res[i:j]
        long_temp.append(section)
        i= j+1
    long = (int(long_temp[0]),int(long_temp[1]))
    contenu = []
    #On enlève les parenthèses parce qu'elles nous gênent
    res = res.replace('(','')
    res = res.replace(')','')
    n = len(res)
    #Maintenant on détermine les valeurs (en niveau de gris) de chaque pixel
    while i<n:
        j = i+1
        section = res[i:j]
        while res[j] != ';':
            j += 1
        section = res[i:j]
        #On a maintenant isolé une section du type '107,103,22' que l'on doit transformer en tuple
        pix = []
        for l in range(2):
            m = 0
            p = 1
            while section[p] != ',':
                p += 1
            pix.append(int(section[m:p]))
            section = section[p+1:]
        pix.append(int(section))
        pix = (pix[0],pix[1],pix[2])
        contenu.append(pix)
        i= j+1
    image_finale = Image.new('RGB',long)
    image_finale.putdata(contenu)
    image_finale.save(chemin+fichier_cible)
    print ("Le fichier a été décodé")

decode_image("image_crypte.txt","codage_image.txt","image_decode.bmp")











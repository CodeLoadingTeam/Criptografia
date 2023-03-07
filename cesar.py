# Cifra de César

alfabeto = 'abcdefghijklmnopqrstuvwyzàáãâéêóôõíúçABCDEFGHIJKLMNOPQRSTUVWYZÀÁÃÂÉÊÓÕÍÚÇ'

# mensagem = 'abelha'
# cifra    = 'cdgnjc' (p/ cada letra, avança 3 caractéres do alfabeto) 

def cripto():
    index=0
    global cifra
    
      # ch = character 
    for ch in input('Digite sua mensagem: '):
            # input: técnicamente, não registraria a mensagem na memória
        if ch in alfabeto:
            index = alfabeto.find(ch) + key
            index = index % len(alfabeto)
            cifra = cifra + alfabeto[index]
                     
        else:
            cifra = cifra + ch  
            
def decripto():
    index=0
    global decifra

    for ch in cifra:

        if ch in alfabeto:
            index = alfabeto.find(ch) - key
            index = index % len(alfabeto)
            decifra = decifra + alfabeto[index]
                    
        else:
            decifra = decifra + ch
            
key = 3 # Chave
cifra, decifra = '','' 

cripto()
print()
print(f'   Criptografada: {cifra}')

decripto()
print(f'Descriptografada: {decifra}')

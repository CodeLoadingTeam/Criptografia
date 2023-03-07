# Bruno's script 

from time import sleep
from string import ascii_uppercase as alpha, printable as alfabeto
from random import choice, randint 

txt = open('relatório.txt', 'w+')
txt.write('''
Uma mensagem foi enviada a um capitão da guarda costeira, a mensagem dizia que um navio vindo da Ásia 
em direção a região norte do Brasil com possível lixo toxico e que ele e sua tripulação deveriam ser 
averiguadas.

Seguindo as normas legislativas, somente inspetores devidamente trajados com roupas especiais poderão 
adentrar o navio, além disso o capitão deixou o navio a uma distância segura de 50 quilômetros da 
costa e todo e qualquer contato deverá ser realizado por meio de helicópteros, para restringir e 
minimizar o contato.

Então seguindo esses meios de restrição o capitão enviou quatro inspetores em um helicóptero para 
averiguar a situação do lixo tóxico e os tripulantes do navio. Para que haja uma comunicação entre a
guarda costeira brasileira e o navio, será estabelecido uma comunicação criptografada assimetricamente 
para saber mais detalhes da situação.
''')

txt.close()


###############################################################################
# transformará p/ binario com um valor puro (sem o '0b' na frente)
def conversorBin(line):
    binario = bin(line).replace('0b','') # retira o '0b' da frente do binario
    
    return binario

# Simula a tabela da verdade para recuperar a quantidade total de caractetes
def tabelaVerdade(qtdeVariaveis):
    
    linhas = 2 ** qtdeVariaveis # base 2 elevado a qtde. de proposições
    random = randint(1,qtdeVariaveis-1)  
    binario = conversorBin(random) # número (random de 0 até linhas)
    
    # Variaveis "qtde" e "qtde_Fim" == qtde. de caracteres que o número possui
    qtde = len(binario)   
    qtde_Fim = len(conversorBin(linhas-1)) # (Pega o n° de linhas da tabela e subtrai por 1)

    if qtde < qtde_Fim:
        diferença = qtde_Fim - qtde
        binario = '0' * diferença + binario
    
    return binario

def cripto(binario):
  code = ''
  um = binario.find('1') 
  index_1 = len(binario[:um]) # qtde de zeros
  index_2 = int(binario,2) -1 
  
  # p/ primeira letra
  if index_1 < len(alpha):
    code = alpha[index_1]
    
  else:
    repetição = 0
    tamanho = len(alpha) # 26

    while tamanho < index_1: 
      repetição += 1 # contador
      tamanho += len(alpha) 
      
    index_1 = index_1 % len(alpha)
    code = str(repetição) + alpha[index_1]
  
  # p/ segunda letra
  if index_2 < len(alpha):    
    code += '-' + str(randint(0,9)) + ('0' * 2) + alpha[index_2]

  else:
    code += '-' + str(randint(0,9))  
    repetição = 0
    tamanho = len(alpha) # 26

    while tamanho < index_2: 
      repetição += 1 # contador
      tamanho += len(alpha) 
      
    repetição = str(repetição)
    diferença = 2 - len(repetição)

    index_2 = index_2 % len(alpha)
    code += ('0' * diferença + repetição) + alpha[index_2]
      
  return code

# Função para gerar a chave
def gerarKey():
  global keys
  z = '\n========================================================================================================\n'
  print(z)
  # quantidade = int(input('Insira o valor a ser usado na encriptação: '))
  for x in range(2): # sendo p/ guarda costeira e p/ navio
    num = tabelaVerdade(40) # chama a função e retorna um número binário
    public_key = cripto(num)
    if x == 0:
      area = 'Guarda costeira'
    else:
      area = 'Navio'

    print(f'{area}, sua chave pública será: ', public_key) 
    keys.append(public_key)

    num = tabelaVerdade(40*2) 
    private_key = cripto(num)
    print('e sua chave privada será: ', private_key) 
    keys.append(private_key)
    print()
  print('(Atenção: para a área A se comunicar com a área B, a mesma deverá utilizar as chaves de B!)')
  print(z)

  # p/ navio
###############################################################################


def relatório():
  txt = open('relatório.txt', 'r')

  for linha in txt.readlines():
    for ch in linha.split():
      print(ch, end = ' ')
      sleep(0.2)  
    print()

  txt.close()


###############################################################################
MODO_ENCRIP = 1
MODO_DECRIP = 0
public_key, private_key, keys, cifra, decifra = '','', [], '',''


def criptografia(modo, key):
    global cifra
    # decifra a quantidade de zeros
    i = key.find('-') - 1
    if key[:i] == '':
      zeros = '0' * alpha.index(key[0])
    else:
      zeros =  ( int(key[:i]) * len(alpha) ) * '0' + '0' * alpha.index(key[1])

    # decifra o número binario
    i = key.find('-') + 2 
    repetições = int(key[i:-1],10) # recupera o número presente na key
    binario = bin(repetições * len(alpha) + alpha.index(key[-1]) + 1) 

    # ajunta ambos os valores e calcula a qtde. de bits
    key = len(zeros + binario.replace('0b','')) # o método replace retira o 0b do número binario
   
    cripto, msg = '',''
    index = 0
    F = modo == MODO_ENCRIP # F = se for ENCRIPTAÇÃO...
    if F:
      while True: 
        msg = input('Digite sua mensagem: ')

        if len(msg) > 128: # for maior que 128
          print('insira uma mensagem na qual tenha menos que 128 caractér')
      
        else: 
          break

    for ch in (msg if F else cifra):

      if ch in alfabeto:
        index = alfabeto.find(ch) + (key*2 if F else -key)
        index = index % len(alfabeto)
        cripto += alfabeto[index]
      else:
        cripto += ch  
        
    del msg
    return cripto
###############################################################################


def encriptação(area_A, area_B):
  global cifra, public_key, private_key
  if area_A == 'Guarda costeira':
    public_key = keys[2]
    private_key = keys[3]
    tal = 'o' # texto para conjunção
  else:
    public_key = keys[0]
    private_key = keys[1]
    tal = 'a'

  imp1 = f'> {area_A}, insira a chave de segurança para enviar sua mensagem para {tal} {area_B}: '
  while True: # 1° Loop
    key = input(imp1)
    if key == public_key: # Chave pública
      cifra = criptografia(MODO_ENCRIP, key)
      print(f'\n   Criptografada: {cifra}')
      print('====================='+ '=' * len(cifra))
      print('\n')
      break # Fecha o 1° Loop

    else: # Chave pública invalida
      print()
      print('A chave de segurança inserida está incorreta!')
      imp1 = f'> {area_A}, insira uma chave de segurança válida para enviar sua mensagem para {tal} {area_B}: '

def decriptação(area_B, area_A):
  global decifra
  if area_B == 'Navio':
    public_key = keys[2]
    private_key = keys[3]
    tal = 'pela' # texto para conjunção
  else:
    public_key = keys[0]
    private_key = keys[1]
    tal = 'pelo' 

  imp2 = f'> {area_B}, insira sua chave de segurança para vizualizar a mensagem encaminhada {tal} {area_A}: '
  while True: # 2° Loop
    key = input(imp2)
    if key == private_key: # Chave privada
      decifra = criptografia(MODO_DECRIP, key)
      print(f'\n   Descriptografada: {decifra}')
      print('========================'+ '=' * len(decifra))
      print('\n')
      break # Fecha o 2° Loop

    else: # Chave privada invalida
      print()
      print('A chave de segurança inserida está incorreta!')
      imp2 = f'> {area_B}, insira uma chave de segurança válida para vizualizar a mensagem encaminhada {tal} {area_A}: '

def mensagens(area_A, area_B):

  encriptação(area_A, area_B)
  sleep(2)

  decriptação(area_B, area_A)
  sleep(2)

###PROCESSO######################################################################


relatório()
sleep(2)

gerarKey() # p/ guarda costeira & p/ navio

for x in range(4):

  if x % 2 == 0: 

    mensagens('Guarda costeira', 'Navio')
  else:

    mensagens('Navio', 'Guarda costeira')

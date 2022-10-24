from cmath import pi
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import sys
import collections
sys.setrecursionlimit(10000000)
velas=[]
ult=[]
gale=[0]*5
acer=[0]*3
banca_inicial=[]
banca_inicial.append(200)
def encontrar_numero(texto):
    if '>0!' in texto:        
        return '2' 
    if '>1!' in texto:        
        return '0'
    if '>2!' in texto:
        return '0'
    if '>3!' in texto:
        return '0'
    if '>4!' in texto:
        return '0'   
    if '>5!' in texto:
        return '0' 
    if '>6!' in texto:
        return '0' 
    if '>7!' in texto:
        return '0' 
    if '>8!' in texto:
        return '1'
    if '>9!' in texto:
        return '1'
    if '>10!' in texto:
        return '1'
    if '>11!' in texto:
        return '1'   
    if '>12!' in texto:
        return '1' 
    if '>13!' in texto:
        return '1' 
    if '>14!' in texto:
        return '1' 
    return 'erro'

def verifica_selecionado():
    black = driver.find_element(By.CLASS_NAME,"black")
    texto=str(black.get_attribute('outerHTML'))
    if 'selected' in texto:        
        return 'black' 
    else:
        return 'red'

def ultima_cor():
    palavra=''    
    while palavra!='Blaze Girou':
        ua = driver.find_element(By.ID,"roulette-timer") 
        texto=str(ua.get_attribute('outerHTML'))          
        if 'Blaze Girou' in texto:
            palavra='Blaze Girou' 
            cor=encontrar_numero(texto)  
            driver.refresh()
            time.sleep(6)
            return cor 
def ultima_cor_res():
    palavra=''    
    while palavra!='Blaze Girou':
        ua = driver.find_element(By.ID,"roulette-timer") 
        texto=str(ua.get_attribute('outerHTML'))          
        if 'Blaze Girou' in texto:
            palavra='Blaze Girou' 
            cor=encontrar_numero(texto)            
            return cor 
def resultado(cor_operada, index,entrada):
    banca=banca_inicial[0]
    print('Aguardando resultado!')
    print('Banca atual: '+str(banca))
    resultado=ultima_cor_res()
    print('Cor operada:'+str(cor_operada)+' Resultado: '+str(resultado))
    if int(resultado)==int(cor_operada):
        # velas.clear()
        banca=banca+(2**index)
        print('Win!')
        acer[0]=acer[0]+1
        print('Banca final: '+str(banca))
        banca_inicial[0]=banca
        # print('Gale 3: '+str(gale[0])+' | Gale 4: '+str(gale[1])+' | Gale 5: '+str(gale[2])+' | Gale 6: '+str(gale[3])+' | Gale 7: '+str(gale[4]))            
        print('------------------------------------------')
        return
    else:
        print('Lose')
        banca=banca-(2**index)
        print('Banca final: '+str(banca))
        banca_inicial[0]=banca
        # cont_gale(index+1)
        acer[1]=acer[1]+1
        if int(index)<1:
            print('Entrando em gale valor: '+str(entrada*2))
            #coresgale(index,entrada*2)            
            operando(cor_operada,index+1,True,entrada)
            return
        acer[2]=acer[2]+1
        # print('Saindo do Gale')
        # print('Perca de: '+str(2**index+1))
        # print('Gale 3: '+str(gale[0])+' | Gale 4: '+str(gale[1])+' | Gale 5: '+str(gale[2])+' | Gale 6: '+str(gale[3])+' | Gale 7: '+str(gale[4]))            
        print('------------------------------------------')
        # velas.clear()
        return
def operando(ultima_vela,gale,gale_true, entrada):    
    ua = driver.find_element(By.ID,"roulette-timer") 
    texto=str(ua.get_attribute('outerHTML'))
    valor=str(entrada)+'.00'     
    if '>3:' in texto: 
        # driver2.refresh()         
        print('operando!')   
        black=driver.find_element(By.XPATH,"//*[@id='roulette']/div/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/div[2]/span")    
        red=driver.find_element(By.XPATH,"//*[@id='roulette']/div/div[2]/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/span")    
        print("Black: "+str(black.text))  
        print("Red:"+str(red.text))
        if(black.text !='R$ NaN'):
            black_num=int(float(black.text.replace('R$ ','')))
            red_num=int(float(red.text.replace('R$ ','')))
            
            if(black_num==0):
                print('nao operou!')
                return
            if int(black_num)>int(red_num):
                cor=1
            else:
                cor=0
        else:
            print('nao operou!')
            return
        elem = driver.find_element(By.CLASS_NAME,"input-field") 
        elem.clear()
        elem.send_keys(valor)
        # page.fill("input[class='input-field']",valor)      
        
        
        # if gale_true==True:
            # cor=ultima_vela
        # cor=velas[-1]
        print('Cor operada: '+ str(cor))                 
        resultado(cor,gale,entrada)
        return  
    else:        
        operando(ultima_vela, gale,gale_true,entrada)
def operar(ultima_vela):
    print('hora de operar')
    acer_total=acer[0]+acer[1]
    print('Acertos: '+str(acer[0])+'x')
    print('Erros: '+str(acer[1])+'x')
    print('Perca Gale: '+str(acer[2])+'x')
    if acer_total>0:
        acertibilidade=int(acer[0]*100/acer_total)        
        print('Acertibilidade: '+str(acertibilidade)+'%')    
    operando(ultima_vela,1,False,2)
def cores():      
    velas.append(ultima_cor())
    operar(velas[-1])
    # if len(velas)>3 :  
        
    #     ult.append(velas[-3])    
    #     ult.append(velas[-2])  
    #     ult.append(velas[-1])     
    #     print(ult)
    #     print(ult.count('1'))
    #     if ult.count('1')>1:
    #         ult.clear()
    #         print(velas)
    #         operar(0)
    #     else:
    #         ult.clear()
    #         print(velas)
    #         operar(1)
    # cor=cor_bot()
    # if cor!=2:
    #     operar(cor)

    return
# def coresgale(index,entrada):      
#     cor=cor_bot()
#     if cor!=2:
#         operando(cor, index+1,True,entrada)
#         return
#     coresgale(index,entrada)
    
    
# def cor_bot():
#     palavra=''    
#     while palavra!='Blaze Girou':
#         ua = driver.find_element(By.ID,"roulette-timer") 
#         texto=str(ua.get_attribute('outerHTML'))
#         time.sleep(1)  
#         if 'Blaze Girou' in texto:
#             palavra='Blaze Girou'
#             button = driver2.find_element(By.CSS_SELECTOR,"img[src*='https://d1muf25xaso8hp.cloudfront.net/https%3A%2F%2Fs3.amazonaws.com%2Fappforest_uf%2Ff1655158849874x780880781531770600%2FBOT%25C3%2583O-NOVO-SISTEMA.png?w=256&h=73&auto=compress&dpr=1&fit=max']")
#             button.click()
#             time.sleep(6)
#             black = driver2.find_element(By.CLASS_NAME,"progress")
#             texto=int(str(black.text).replace('%', ''))
#             print(int(texto))
#             if int(texto)<=50:
#                 return 0                    
#             elif texto>=51:
#                 return 1  
#             else:
#                 return 2
                    
            

driver= webdriver.Chrome(executable_path=r'./chromedriver')
driver.get('https://blaze.com/pt/games/double')
# driver2= webdriver.Chrome(executable_path=r'./chromedriver')
# driver2.get('https://sistemabotmachine.com/bot')
input('logar no bot:')
print('logado!')
i=0
while (i<1):           
    cores()



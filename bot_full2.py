#!/usr/bin/python3
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import time
import sys

def stop(lucro, gain, loss):
	if lucro <= float('-' + str(abs(loss))):
		print('Stop Loss batido!')
		while True:
			saida = input('Digite s para sair:').upper()
			if saida == 'S':
				sys.exit()
	if lucro >= float(abs(gain)):
		print('Stop Gain Batido!')
		while True:
			saida = input('Digite s para sair:').upper()
			if saida == 'S':
				sys.exit()

def Payout(par):
	API.subscribe_strike_list(par, 1)
	while True:
		d = API.get_digital_current_profit(par, 1)
		if d != False:
			d = round(int(d) / 100, 2)
			break
		time.sleep(1)
	API.unsubscribe_strike_list(par, 1)
	
	return d

def Martingale(valor, payout):
	lucro_esperado = valor * payout
	perca = float(valor)	
		
	while True:
		if round(valor * payout, 2) > round(abs(perca) + lucro_esperado, 2):
			return round(valor, 2)
			break
		valor += 0.01


def VerificaTendencia(total, qtd_velas):
	percentual_verde = round((total.count('g') * 100) / (qtd_velas-1))
	percentual_vermelha = round((total.count('r') * 100) / (qtd_velas-1))

	if percentual_verde > 60:
		tendencia = 'call'
	elif percentual_vermelha > 60:
		tendencia = 'put'
	else:
		tendencia = 'neutro'

	return tendencia


#Verifica se está em OTC, se estiver muda a estrategia de operação:
def VerificaOperacao(penta, quadra, triple, total, velas, qtd_velas, paridade):
	result = []
	tendencia = VerificaTendencia(total, qtd_velas)

	'''
	if paridade[7:10] == 'OTC':
	result = [paridade, 'put', penta]
	result = [paridade, 'call', penta]

	
	'''

	g = total.count(triple + 'g')
	r = total.count(triple + 'r')

	if g == 0 and r == 2 and tendencia == 'call':
		result = [paridade, 'call', penta]
	elif g == 2 and r == 0 and tendencia == 'put':
		result = [paridade, 'put', penta]
	else:
		pass


	return result


def Operacao(par, paridade_removida):
	dir = False
	qtd_velas = 16
	result = []

	for paridade in par['digital']:
		if par['digital'][paridade]['open'] == True and paridade not in ('GBPJPY-OTC', 'USDZAR-OTC', 'USDSGD-OTC', 'USDHKD-OTC', 'USDINR-OTC', 'GBPUSD'):
			velas = ' '
			total = ' '
			velas = API.get_candles(paridade, 60, qtd_velas, time.time())
			for i in range(qtd_velas):
				velas[i] = 'g' if velas[i]['open'] < velas[i]['close'] else 'r' if velas[i]['open'] > velas[i]['close'] else 'd'
				if i != (qtd_velas-1):
					total = total + velas[i]

			penta = ' '
			quadra = ' '
			triple = ' '
			triple = velas[qtd_velas-4] + velas[qtd_velas-3] + velas[qtd_velas-2]
			quadra = velas[qtd_velas-5] + ' ' + velas[qtd_velas-4] + ' ' + velas[qtd_velas-3] + ' ' + velas[qtd_velas-2]
			penta = velas[qtd_velas-6] + ' ' + velas[qtd_velas-5] + ' ' + velas[qtd_velas-4] + ' ' + velas[qtd_velas-3] + ' ' + velas[qtd_velas-2]

			if penta.count('d') >= 1 or penta.count('g') == 5 or penta.count('r') == 5:
				continue

			result = VerificaOperacao(penta, quadra, triple, total, velas, qtd_velas, paridade)

			if result != []:
				break
	
	if len(result) != 0 and paridade_removida != result[0]:
		if paridade[7:10] == 'OTC':
			print('\nOperando em OTC...')
		print('\nVerificando cores...\n', end='')
		print(result[2])
		print('Paridade: ', result[0])
		print('Direção:',result[1])
	else:
		print ('\nNenhum padrão de velas encontradas...\n')

	return result


while True:
	#login = input('Informe o seu login: ')
	#senha = input('Informe sua senha: ')
	login = 'leop.gabriel9@gmail.com'
	senha = 'Nossamae123'
	API = IQ_Option(login, senha)
	API.connect()
	if API.check_connect():
		print('Conectado com sucesso!')
		break
	else:
		print(' Erro ao conectar... Digite novamente...')

API.change_balance('PRACTICE') # PRACTICE / REAL

while True:
	try:
		operacao = 1
		
		if operacao > 0 and operacao < 3 : break
	except:
		print('\n Opção invalida')

valor_entrada = 2
valor_entrada_b = float(valor_entrada)

martingale = 8
martingale += 1

stop_loss = 1100
stop_gain = 500

lucro = 0
max_mg = 0
qtd_mg = 0

while True:
	minutos = float(((datetime.now()).strftime('%M.%S'))[2:])
	entrar = True if (minutos >= 0.05 and minutos <= 0.1) else False
	tempo=int(minutos*100)	
	if tempo%10 == 0 or entrar== True:
		print('Hora de entrar?',entrar,'/ Minutos:',minutos, '/ Lucro:', round(lucro, 2), '/ Max MG:', max_mg, ':',qtd_mg,'x')

	if entrar:
		paridade_removida = ''
		par = API.get_all_open_time()
		result = Operacao(par, paridade_removida)
		if len(result) != 0:
			dir = result[1]
			paridade = result[0]
			payout = Payout(paridade)
		else:
			dir = False

		if dir:
			print('Iniciando operação!\n')
			valor_entrada = valor_entrada_b
			#for i in range(martingale):
			i = 0
			while i < martingale:

				if i != 0 and i > max_mg: 
					max_mg = i
					qtd_mg = 0
				if i != 0 and i == max_mg: 
					qtd_mg += 1
	
				if i > 0:
					paridade_removida = paridade
					dir = False
					while True:
						try:
							minutos2 = float(((datetime.now()).strftime('%M.%S'))[2:])
							entrar2 = True if (minutos2 >= 0.05 and minutos2 <= 0.1) else False
							if entrar2:
								print('\nHora de entrar?',entrar2,'/ Minutos:',minutos2, '/ Lucro:', round(lucro, 2), '/ GALE: ' + str(i), '/ Max MG:', max_mg, ':',qtd_mg,'x')
								par = API.get_all_open_time()
								result = Operacao(par, paridade_removida)
								if len(result) != 0:
									dir = result[1]
									paridade = result[0]
						except:
							minutos2 = float(((datetime.now()).strftime('%M.%S'))[2:])
							entrar2 = True if (minutos2 >= 0.05 and minutos2 <= 0.1) else False
							if entrar2:
								print('\nHora de entrar?',entrar2,'/ Minutos:',minutos2, '/ Lucro:', round(lucro, 2), '/ GALE: ' + str(i), '/ Max MG:', max_mg, ':',qtd_mg,'x')
								par = API.get_all_open_time()
								result = Operacao(par, paridade_removida)
								if len(result) != 0:
									dir = result[1]
									paridade = result[0]
						finally:
							if dir != False and paridade_removida != paridade:
								break
							else: 
								time.sleep(0.5)

				status,id = API.buy_digital_spot(paridade, valor_entrada, dir, 1) if operacao == 1 else API.buy(valor_entrada, paridade, dir, 1)

				if status:
					while True:
						try:
							#status,valor = API.check_win_digital_v2(id) if operacao == 1 else True, API.check_win_v3(id)
							status,valor = API.check_win_digital_v2(id) if operacao == 1 else API.check_win_v3(id)
						except:
							status = True
							valor = 0
						
						if status:
							valor = valor if valor > 0 else float('-' + str(abs(valor_entrada)))
							lucro += round(valor, 2)
							
							print('Resultado operação: ', end='')
							print('WIN /' if valor > 0 else 'LOSS /' , round(valor, 2) ,'/ Lucro:', round(lucro, 2),('/ '+str(i)+ ' GALE' if i > 0 else '' ))
							
							valor_entrada = Martingale(valor_entrada, payout)
	
							stop(lucro, stop_gain, stop_loss)
							
							break

					if valor > 0: 
						break
					
				else:
					if i > 0:
						i = i - 1 #pra não bugar o martingale
					print('\nERRO AO REALIZAR OPERAÇÃO\n\n')
					print('\nRetornando operações em 2 minutos...')
					time.sleep(180)

				i = i + 1

	time.sleep(0.5)

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


def VerificaOperacao(penta, triple, total, velas, qtd_velas, paridade):
	result = []
	vela_atual = API.get_candles(paridade, 60, 1, time.time())

	if triple.count('g') < triple.count('r') and vela_atual[0]['open'] < vela_atual[0]['close']:
		estrategia = 'MHI / velas verdes sao a minoria'
		result = [paridade, 'call', penta, estrategia]

	elif triple.count('r') < triple.count('g') and vela_atual[0]['open'] > vela_atual[0]['close']:
		estrategia = 'MHI / velas vermelhas sao a minoria'
		result = [paridade, 'put', penta, estrategia]

	else:
		pass

	
	return result


def Operacao(par):
	qtd_velas = 7
	result = []

	for paridade in par['digital']:
		if par['digital'][paridade]['open'] == True and paridade not in ('GBPJPY-OTC', 'USDZAR-OTC', 'USDSGD-OTC', 'USDHKD-OTC', 'USDINR-OTC', 'GBPUSD', 'NZDUSD-OTC'):
			total = ' '
			velas = API.get_candles(paridade, 60, qtd_velas, time.time())

			for i in range(qtd_velas):
				velas[i] = 'g' if velas[i]['open'] < velas[i]['close'] else 'r' if velas[i]['open'] > velas[i]['close'] else 'd'
				if i != (qtd_velas-1):
					total = total + velas[i]

			minutos = float(((datetime.now()).strftime('%M.%S'))[2:])
			if minutos > 0.26:
				break

			penta = ''
			penta = velas[qtd_velas-6] + ' ' + velas[qtd_velas-5] + ' ' + velas[qtd_velas-4] + ' ' + velas[qtd_velas-3] + ' ' + velas[qtd_velas-2]
			#quadra = ''
			#quadra = velas[qtd_velas-5] + ' ' + velas[qtd_velas-4] + ' ' + velas[qtd_velas-3] + ' ' + velas[qtd_velas-2]
			triple = ''
			triple = velas[qtd_velas-4] + velas[qtd_velas-3] + velas[qtd_velas-2]
			#hexa = ''
			#hexa = velas[qtd_velas-7] + velas[qtd_velas-6] + velas[qtd_velas-5] + velas[qtd_velas-4] + velas[qtd_velas-3] + velas[qtd_velas-2]

			if penta.count('d') >= 1 or penta.count('g') == 5 or penta.count('r') == 5 or triple.count('g') == 3 or triple.count('r') == 3:
				continue

			else:
				result = VerificaOperacao(penta, triple, total, velas, qtd_velas, paridade)
				

			if result != []:
				break
	
	if len(result) != 0:
		if paridade[7:10] == 'OTC':
			print('\nOperando em OTC...')
		print('\nVerificando cores...\n', end='')
		print(result[2])
		print('Paridade: ', result[0])
		print('Estrategia: ', result[3])
		print('Direção:',result[1])
	else:
		print ('\nNenhum padrao de velas encontrado...\n')

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

valor_entrada = 10
valor_entrada_b = float(valor_entrada)

martingale = 0
martingale += 1

stop_loss = 200
stop_gain = 1000

lucro = 0
max_mg = 0
qtd_mg = 0
win = 0
loss = 0

while True:
	minutos = float(((datetime.now()).strftime('%M.%S'))[2:])
	entrar = True if (minutos >= 0.15 and minutos <= 0.16) else False
	tempo=int(minutos*100)	
	if tempo%10 == 0 or entrar== True:
		print('Hora de entrar?',entrar,'/ Minutos:',minutos, '/ Lucro:', round(lucro, 2), '/ Max MG:', max_mg, ':',qtd_mg,'x')

	if entrar:
		par = API.get_all_open_time()
		result = Operacao(par)
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

				if i >= 3:
					#Salva o horario do maior Martin Gale:
					minutos = ((datetime.now()).strftime('%A - %H.%M.%S'))
					dados = 'Gale ' + str(i) + ': ' + minutos + ' / Paridade: ' + str(paridade) + ' / Estrategia: ' + result[3] + ' Velas: ' + result[2]
					f = open("horarios_gale_bot_mhi.txt", "a")
					f.write(dados)
					f.write('\n')
					f.close()
	
				if i > 3:	
					dir = False

					while True:
						try:
							minutos2 = float(((datetime.now()).strftime('%M.%S'))[2:])
							entrar2 = True if (minutos2 >= 0.15 and minutos2 <= 0.16) else False
							if entrar2:
								print('\nHora de entrar?',entrar2,'/ Minutos:',minutos2, '/ Lucro:', round(lucro, 2), '/ GALE: ' + str(i), '/ Max MG:', max_mg, ':',qtd_mg,'x')
								par = API.get_all_open_time()
								result = Operacao(par)
								if len(result) != 0:
									dir = result[1]
									paridade = result[0]
						except:
							minutos2 = float(((datetime.now()).strftime('%M.%S'))[2:])
							entrar2 = True if (minutos2 >= 0.15 and minutos2 <= 0.16) else False
							if entrar2:
								print('\nHora de entrar?',entrar2,'/ Minutos:',minutos2, '/ Lucro:', round(lucro, 2), '/ GALE: ' + str(i), '/ Max MG:', max_mg, ':',qtd_mg,'x')
								par = API.get_all_open_time()
								result = Operacao(par)
								if len(result) != 0:
									dir = result[1]
									paridade = result[0]
						finally:
							if dir != False:
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
							
							print('----------------------------')
							if valor > 0:
								win += 1
							else:
								loss += 1
								minutos = ((datetime.now()).strftime('%A - %H.%M.%S'))
								dados = 'LOSS / ' + minutos + ' / Paridade: ' + str(paridade) + ' / Estrategia: ' + result[3] + ' Velas: ' + result[2] + ' / Wins: ' + str(win) + ' Losses: ' + str(loss)
								f = open("bot_mhi2_sem_gale_losses.txt", "a")
								f.write(dados)
								f.write('\n')
								f.close()

							print('Wins: ', win, ' | Losses: ', loss)
							acertividade = (win * 100) / (win + loss)
							print('Acertividade: ', round(acertividade, 2), '%')
							print('----------------------------')
							print('\n')

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
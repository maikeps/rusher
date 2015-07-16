# coding: utf-8

import json
from pprint import pprint

courses = {
	# Código : [Nome, H/A, Aulas, Pré-Requisitos]

	# Fase 01
	'EEL5105' : ['Circuitos e Técnicas Digitais', 90, 5, []],
	'INE5401' : ['Introdução à Computação', 36, 2, []],
	'INE5402' : ['Programação Orientada a Objetos I', 108, 6, []],
	'INE5403' : ['Fundamentos de Matemática Discreta para Computação', 108, 6, []],
	'MTM5161' : ['Cálculo A', 72, 4, []],

	# Fase 02
	'INE5404' : ['Programação Orientada a Objetos II', 108, 6, ['INE5402']],
	'INE5405' : ['Probabilidade e Estatística', 90, 5, ['MTM5161']],
	'INE5406' : ['Sistemas Digitais', 90, 5, ['EEL5105']],
	'INE5407' : ['Ciência, Tecnologia e Sociedade', 54, 3, []],
	'MTM5512' : ['Geometria Analítica', 72, 4, []],
	'MTM7174' : ['Cálculo B para Computação', 72, 4, ['MTM5161']],

	# Fase 03
	'INE5408' : ['Estruturas de Dados', 108, 6, ['INE5404']],
	'INE5409' : ['Cálculo Numérico para Computação', 72, 4, ['MTM5512', 'MTM7174']],
	'INE5410' : ['Programação Concorrente', 72, 4, ['INE5404']],
	'INE5411' : ['Organização de Computadores I', 108, 6, ['INE5406']],
	'MTM5245' : ['Álgebra Linear', 72, 4, ['MTM5512']],

	# Fase 04
	'INE5412' : ['Sistemas Operacionais I', 72, 4, ['INE5410', 'INE5411']],
	'INE5413' : ['Grafos', 72, 4, ['INE5403', 'INE5408']],
	'INE5414' : ['Redes de Computadores I', 72, 4, ['INE5404']],
	'INE5415' : ['Teoria da Computação', 72, 4, ['INE5403', 'INE5408']],
	'INE5416' : ['Paradigmas de Programação', 90, 5, ['INE5408']],
	'INE5417' : ['Engenharia de Software I', 90, 5, ['INE5408']],

	# Fase 05
	'INE5418' : ['Computação Distribuída', 72, 4, ['INE5412', 'INE5414']],
	'INE5419' : ['Engenharia de Software II', 72, 4, ['INE5417']],
	'INE5420' : ['Computação Gráfica', 72, 4, ['INE5408', 'MTM5245', 'MTM7174']],
	'INE5421' : ['Linguagens Formais e Compiladores', 72, 4, ['INE5415']],
	'INE5422' : ['Redes de Computadores II', 72, 4, ['INE5414']],
	'INE5423' : ['Banco de Dados I', 72, 4, ['INE5408']],
	
	# Fase 06
	'INE5424' : ['Sistemas Operacionais II', 72, 4, ['INE5412']],
	'INE5425' : ['Modelagem e Simulação', 72, 4 , ['INE5405']],
	'INE5426' : ['Construção de Compiladores', 72, 4, ['INE5421']],
	'INE5427' : ['Planejamento e Gestão de Projetos', 72, 4 , ['INE5417']],
	'INE5430' : ['Inteligência Artificial', 72, 4, ['INE5405', 'INE5413', 'INE5416']],
	'INE5453' : ['Introdução ao Trabalho de Conclusão de Curso', 18, 1 , ['INE5417']],

	# Fase 07
	'INE5428' : ['Informática e Sociedade', 72, 4, ['INE5407']],
	'INE5429' : ['Segurança em Computação', 72, 4, ['INE5403', 'INE5414']],
	'INE5431' : ['Sistemas Multimídia', 72, 4, ['INE5414']],
	'INE5432' : ['Banco de Dados II', 72, 4, ['INE5423']],
	'INE5433' : ['Trabalho de Conclusão de Curso I (TCC)', 108, 6, ['INE5427', 'INE5453']],
	# +2 Opt

	# Fase 08
	'INE5434' : ['Trabalho de Conclusão de Curso II (TCC)', 162, 9, ['INE5433']],
	# +2 Opt

}

def get_name(code):
	return courses[code][0]

def get_hours(code):
	return courses[code][1]

def get_classes_week(code):
	return courses[code][2]

def get_dependencies(code):
	return courses[code][3]

def get_schedule(code):
	schedule_aux = courses[code][4]
	schedule = []
	for item in schedule_aux:
		class_day = []
		for i in range(len(item)):
			aux = item[i].encode('utf8')[:8:]
			day = aux[0]
			start_hour = int(aux[2:4])
			start_min = int(aux[4:6])
			hours = int(aux[7])

			offset = 50*hours
			plus_hours = int(offset/60)
			plus_min = offset % 60

			end_hour = start_hour + plus_hours
			end_min = (start_min + plus_min) % 60
			if(start_min + plus_min >= 60):
				end_hour += 1

			if(end_hour > 16):
				end_min = (end_min + 20) % 60
				if int((end_min+20)/60) % 60 == 0:
					end_hour += 1

			start = str(start_hour) + str(start_min).zfill(2)
			end = str(end_hour) + str(end_min).zfill(2)

			class_day.append((day, start, end))
		schedule.append(class_day)
	return schedule

def update_classes(semester, campus):
	filename = "db/"+semester+"_"+campus+".json"
	f = open(filename, 'r')
	data = json.load(f)
	# pega todas as materias do campus
	for course in data[campus]:
		# itera sobre todas as materias de cco
		code = course[0].encode('utf8')
		try:
			cco_course = courses[code]
		except:
			continue
		schedule = []
		for option in course[3]:
			schedule.append(option[7])
		courses[code].append(schedule)

update_classes('20152', 'FLO')
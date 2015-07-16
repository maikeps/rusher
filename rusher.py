#!/usr/bin/env python3
# coding: utf-8

from courses_cco import courses, get_name, get_hours, get_classes_week, get_dependencies, get_schedule
from graph import Graph, Node

def build_graph():
	g = Graph(True)
	for course in courses:
		g.add_node(Node(course, courses[course]))
	for course in courses:
		for next_course in get_dependencies(course):
			g.connect(course, next_course)

	return g

g = build_graph()

final_course = 'INE5434'
min_hours = 12
max_hours = 28

def get_available_options(completed_courses):
	options = []
	for course in courses:
		if course not in completed_courses:
			if get_dependencies(course) == []:
				options.append(course)
			else:
				dep_set = set(get_dependencies(course))
				completed_set = set(completed_courses)
				if dep_set.issubset(completed_set):
					options.append(course)
	return options

def check_min_hours(plan, new_course):
	hours = get_classes_week(new_course)
	for course in plan:
		hours += get_classes_week(course)
	return hours >= min_hours

def check_max_hours(plan, new_course):
	hours = get_classes_week(new_course)
	for course in plan:
		hours += get_classes_week(course)
	return hours <= max_hours

def build_plan(completed_courses):
	completed_courses_aux = completed_courses
	options = get_available_options(completed_courses_aux)
	magnitudes = get_courses_magnitude(options)

	plans = []
	while not all_courses_completed(completed_courses_aux):
		# most important courses sorted by magnitude
		courses_sorted = sorted(magnitudes.keys(), key=lambda x: magnitudes[x])[::-1]
		plan = []
		new_course = courses_sorted[0]
		print(courses_sorted)
		while (not check_min_hours(plan, new_course)) or check_max_hours(plan, new_course):
			try:
				if not conflicts(new_course, plan):
					plan.append(new_course)

				del courses_sorted[0]
				new_course = courses_sorted[0]
			except:
				break
		plans.append(plan)
	
		for item in plan:
			completed_courses_aux.append(item)
	
		options = get_available_options(completed_courses_aux)
		magnitudes = get_courses_magnitude(options)		

	return plans

def conflicts(course, plan):
	course_schedule = get_schedule(course)
	
	# para cada materia presente no plano
	for aux in plan:
		conflict_count = 0
		aux_schedule = get_schedule(aux)

		# itera sobre as diferentes turmas existentes
		count = 0
		for course_schedule_aux in course_schedule:
			# itera sobre as turmas existentes de cada materia existente no plano
			for course_option in course_schedule_aux:
				
				for aux_schedule_aux in aux_schedule:
					for aux_option in aux_schedule_aux:
						day_a = int(aux_option[0])
						start_a = int(aux_option[1])
						end_a = int(aux_option[2])
						day_b = int(course_option[0])
						start_b = int(course_option[1])
						end_b = int(course_option[2])

						# if day_b == day_a and ((start_a > start_b and start_a < end_b) or (start_b > start_a and start_b < end_a) or start_a == start_b or end_a == end_b):
						A = start_a >= end_b
						B = end_a <= start_b
						if day_b == day_a and not A and not B:
							conflict_count += 1
							break
				print(len(aux_schedule), conflict_count)
				if conflict_count == len(aux_schedule):
					count += 1
		if count >= len(course_schedule):
			return True
	return False

def get_courses_magnitude(remaining_courses):
	magnitudes = {x:0 for x in remaining_courses}
	for course in remaining_courses:
		magnitudes[course] = len(get_blocked_courses(course))
	return magnitudes

def get_blocked_courses(course):
	return g.path_to_end(course)


def all_courses_completed(completed_courses):
	return get_available_options(completed_courses) == [] and final_course in completed_courses


completed_courses = ['EEL5105', 'INE5401', 'INE5402', 'INE5403', 'MTM5161']
# completed_courses = ['EEL5105', 'INE5401', 'INE5402', 'INE5403', 'MTM5161', 'INE5404', 'INE5405','INE5406','INE5407','MTM5512','MTM7174','INE5408','INE5410','INE5411','MTM5245','INE5413','INE5414','INE5415','INE5416','INE5417','INE5419']

# plans = []
plans = build_plan(completed_courses)

for i in range(len(plans)):
	semester = plans[i]
	hours = 0
	string = str(i+1) + "º semestre:\n"
	for j in range(len(semester)):
		course = semester[j]
		# string += get_name(course)
		string += course
		if j < len(semester)-1:
			string += ", "
		hours += get_classes_week(course)
	string += "\n"+str(hours)+" horas/semana\n"
	print(string)

# ta feio, ta rude
def get_most_important_courses():
	a = []
	for b in courses:
		a.append(b)
	magnitudes = get_courses_magnitude(a)
	sort = sorted(magnitudes.keys(), key=lambda x: magnitudes[x])[::-1]

	rank = []
	for item in sort:
		if item not in rank:
			rank.append(item)
			print("("+ item + ") " + get_name(item) +": "+ str(magnitudes[item]))
		aux = get_blocked_courses(item)
		for i in aux:
			rank.append(i)
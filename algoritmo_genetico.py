# #-encoding: utf-8
# Algoritmo genético TFG

# Cada cromosoma es una lista de números que representa
# la siguiente información:
# - La información de cada profesor se almacena durante 8*5 posiciones
# de la lista, siendo 5 el numero de dias de la semana laboral
#
# - Cada posición de la lista se corresponde con una franja horaria
#
# - Cada número de la lista se corresponde con una asignatura
# siendo 0 hora libre.

# En este archivo se destacan los siguientes métodos
# -inputData
# -initPopulation
# -crosover
# -mutation
# -fitness
# -selection

# import numpy.random as nprnd
import random
import fileparser
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict
#import time
#import threading

# Inicializacion del programa
NUM_GENERATIONS = 100
TAM_POPULATION = 1000
PROB_MUTATION = 10
# # atributos metodo selection
PERC_POP = 100
PERC_RANDOM = 30
# # end atributos metodo selection
# # atributos metodo crossover
PERC_POP_CROS = 80
# # end atributos metodo crossover
PARSE_ASSIGNMENTS = defaultdict(set)
SUBJECTS = [0]  # Inicializamos con 0 que representa hora libre
SUBJECTS_REPETITIONS = defaultdict(int)
PROFESSORS = []
# Variables que guardaran la informacion recogida del archivo .txt, incicializandolas 0
SUBJECTS_NUMBER = 0
PROFESSOR_NUMBER = 0


# ######## FILE PARSER ##########

# # parse file to get initial data

class subject():
    def __init__(self, name, group):
        self.name = name
        self.group = group


def read_assignments(FILENAME):
    """ Returns profs_asg which corresponds to a defaultdict whose keys
    represents professor names and its values are related to the subjects that they have"""
    profs_asg = defaultdict(set)
    with open(FILENAME) as p:
        for line in p.readlines():
            if line[0] == ':':
                professor = line[1:-1]
            else:
                repetitions = line.split()
                len = int(repetitions.__len__() / 2)
                for n in range(len):
                    subjectName = repetitions.pop(0)
                    group = repetitions.pop(0)
                    subj = subject(subjectName, group)
                    profs_asg[professor].add(subj)
    for key, value in profs_asg.items():
        print("\n")
        print("Teacher " + key + " has assigned the following subjects:")
        for subj in value:
            print(subj.name + ' group ' + subj.group)
    return profs_asg


# ########### END FILE PARSER #########




def initialize(FILENAME):
    n = 0
    pos = 1
    subjs = []
    global PROFESSOR_NUMBER

    ASSIGNMENTS = fileparser.read_assignments(
        FILENAME)  # Cargamos los datos de inicio desde un archivo .txt utilizando un archivo python externo
    for prof, subjects in ASSIGNMENTS.items():

        PROFESSORS.append(prof)
        PARSE_ASSIGNMENTS[n].add(0)

        for elem in subjects:
            # if str(elem.name + elem.group) not in subjs:
            # subjs.append(str(elem.name + elem.group))
            # id = str((subjs.index(str(elem.name + elem.group)) + 1)*10) + '0' + str(
            # pos)
            id = str(elem.name + elem.group)
            PARSE_ASSIGNMENTS[n].add(
                id)  # estamos asignando a cada profesor un identificador unico, asi como a cada subj que posee.
            SUBJECTS.append(elem)
            print(elem.name + ' ' + elem.group + ' se corresponde con el id ' + id)
            pos += 1
        n += 1
    SUBJECTS_NUMBER = SUBJECTS.__len__()
    # print(PARSE_ASSIGNMENTS)
    
    for key in ASSIGNMENTS.keys():
        PROFESSOR_NUMBER += 1
    return ASSIGNMENTS


def initialize_attributes():
    NUM_GENERATIONS = int(input("Inserte el numero de generaciones a crear"))
    TAM_POPULATION = int(input("Inserte la poblacion"))
    PROB_MUTATION = int(input("Inserte la probabilidad de mutacion"))
    PERC_POP = int(input("Inserte el porcentaje de la poblacion que pasara al proceso de seleccion"))
    PERC_RANDOM = int(input("Inserte el porcentaje de la poblacion que sera seleccionada de forma aleatoria "))


# Help methods for phenotype
# # subject parser

def parse_professor(data):
    """ Data: dict {profID : [subjID1,subjID2..],[subjIDX,subjIDX+1..] """
    res = dict()
    for prof, values in data.items():
        professor = PROFESSORS[prof]  # obtenemos el nombre del profesor
        prof_subj = []
        for day in values:
            for subj in day:
                if subj == 0:
                    prof_subj.append('Libre')  # hora libre
                else:

                    prof_subj.append(
                        subj[0:-2] + ' ' + subj[-2::])  # obtenemos nombre de cada asignatura
            res.update({professor: prof_subj})
    return res

    # # end help methods for phenotype


def inputData():
    professor_number = int(input("Introduzca el número de profesores"))

    return professor_number


def initIndividual(ASSIGNMENTS):
    """ Generates random data for the individual solution """
    # MAXIMUM_HOURS_BY_LAW = 3  # Numero maximo de asignaturas que puede, por ley, impartir un profesor por dia
    HOURS_PER_DAY = 8
    ind = list()
    zeros = [0]
    n = 0
    for prof, subjects in ASSIGNMENTS.items():
        aux = list()
        for elem in subjects:
            aux.append(str(elem.name) + str(elem.group))

        for elem in aux:
            SUBJECTS_REPETITIONS[elem] = aux.count(elem)

        random.shuffle(aux)
        aux2 = []
        week = []
        monday = []
        tuesday = []
        wednesday = []
        thursday = []
        friday = []

        for n in range(4):
            if aux.__len__() > 0:
                if aux[0] not in monday:
                    monday.append(aux.pop(0))
        monday += (6 - monday.__len__()) * zeros
        random.shuffle(monday)

        for n in range(4):
            if aux.__len__() > 0:
                if aux[0] not in tuesday:
                    tuesday.append(aux.pop(0))
        tuesday += (6 - tuesday.__len__()) * zeros
        random.shuffle(tuesday)

        for n in range(4):
            if aux.__len__() > 0:
                if aux[0] not in wednesday:
                    wednesday.append(aux.pop(0))
        wednesday += (6 - wednesday.__len__()) * zeros
        random.shuffle(wednesday)

        for n in range(4):
            if aux.__len__() > 0:
                if aux[0] not in thursday:
                    thursday.append(aux.pop(0))
        thursday += (6 - thursday.__len__()) * zeros
        random.shuffle(thursday)

        for n in range(4):
            if aux.__len__() > 0:
                if aux[0] not in friday:
                    friday.append(aux.pop(0))
        friday += (6 - friday.__len__()) * zeros
        random.shuffle(friday)

        ind += monday + tuesday + wednesday + thursday + friday

    return ind


def phenotype(genotype):
    BY_PROFESSOR = list()
    BY_DAY_PROFESSOR = list()
    PROFESSOR_WEEK = dict()
    for num in range(PROFESSOR_NUMBER):
        fin = (num + 1) * 30  # TODO aqui se ha tomado 8 como numero de asignaturas
        ini = num * 30
        BY_PROFESSOR.append(genotype[ini:fin])
    count = 0
    for prof in BY_PROFESSOR:
        BY_DAY_PROFESSOR.append(prof[:6])
        BY_DAY_PROFESSOR.append(prof[6:12])
        BY_DAY_PROFESSOR.append(prof[12:18])
        BY_DAY_PROFESSOR.append(prof[18:24])
        BY_DAY_PROFESSOR.append(prof[24:30])
        PROFESSOR_WEEK.update({count: BY_DAY_PROFESSOR})
        BY_DAY_PROFESSOR = list()
        count = count + 1
    return parse_professor(PROFESSOR_WEEK)


def initPopulation(asgmnts):
    return [initIndividual(asgmnts) for _ in range(TAM_POPULATION)]


def mutation_day(chromosome):
    ini = 0
    fin = 0

    for prof in range(PROFESSOR_NUMBER):
        checkprob = random.randint(0, 100)
        if checkprob <= PROB_MUTATION:
            days_to_change = random.sample(range(5), 2)
            first_day_start = 30 * days_to_change[0]
            first_day_end = first_day_start + 30
            first_day = list(chromosome[first_day_start:first_day_end])

            second_day_start = 30 * days_to_change[1]
            second_day_end = second_day_start + 30
            second_day = list(chromosome[second_day_start:second_day_end])

            chromosome[first_day_start:first_day_end] = second_day
            chromosome[second_day_start:second_day_end] = first_day


def mutation_hour(chromosome):
    ini = 0
    fin = 0
    for prof in range(PROFESSOR_NUMBER):
        for i in range(0 + ini, 6 + fin - 1):

            checkprob = random.randint(0, 100)
            if checkprob <= PROB_MUTATION:
                rand1 = random.randint(0 + ini, 6 + fin - 1)
                rand2 = random.randint(0 + ini, 6 + fin - 1)
                # UTILIZO randint porque sample no me deja especificar el rango concreto de numeros, es decir, de 5 a 10 por ejemplo, sino que es un rango tal que range(200)
                while rand1 == rand2:
                    rand2 = random.randint(0 + ini, 6 + fin - 1)
                h1 = chromosome[rand1]
                h2 = chromosome[rand2]
                chromosome[rand2] = h1
                chromosome[rand1] = h2
                # Se intercambian horas del mismo dia

        for i in range(6 + ini, 12 + fin - 1):

            checkprob = random.randint(0, 100)
            if checkprob <= PROB_MUTATION:
                rand1 = random.randint(6 + ini, 12 + fin - 1)
                rand2 = random.randint(6 + ini, 12 + fin - 1)
                # UTILIZO randint porque sample no me deja especificar el rango concreto de numeros, es decir, de 5 a 10 por ejemplo, sino que es un rango tal que range(200)
                while rand1 == rand2:
                    rand2 = random.randint(6 + ini, 12 + fin - 1)
                h1 = chromosome[rand1]
                h2 = chromosome[rand2]
                chromosome[rand2] = h1
                chromosome[rand1] = h2

        for i in range(12 + ini, 18 + fin - 1):

            checkprob = random.randint(0, 100)
            if checkprob <= PROB_MUTATION:
                rand1 = random.randint(12 + ini, 18 + fin - 1)
                rand2 = random.randint(12 + ini, 18 + fin - 1)
                # UTILIZO randint porque sample no me deja especificar el rango concreto de numeros, es decir, de 5 a 10 por ejemplo, sino que es un rango tal que range(200)
                while rand1 == rand2:
                    rand2 = random.randint(12 + ini, 18 + fin - 1)
                h1 = chromosome[rand1]
                h2 = chromosome[rand2]
                chromosome[rand2] = h1
                chromosome[rand1] = h2

        for i in range(18 + ini, 24 + fin - 1):

            checkprob = random.randint(0, 100)
            if checkprob <= PROB_MUTATION:
                rand1 = random.randint(18 + ini, 24 + fin - 1)
                rand2 = random.randint(18 + ini, 24 + fin - 1)
                # UTILIZO randint porque sample no me deja especificar el rango concreto de numeros, es decir, de 5 a 10 por ejemplo, sino que es un rango tal que range(200)
                while rand1 == rand2:
                    rand2 = random.randint(18 + ini, 24 + fin - 1)
                h1 = chromosome[rand1]
                h2 = chromosome[rand2]
                chromosome[rand2] = h1
                chromosome[rand1] = h2

        for i in range(24 + ini, 30 + fin - 1):

            checkprob = random.randint(0, 100)
            if checkprob <= PROB_MUTATION:
                rand1 = random.randint(24 + ini, 30 + fin - 1)
                rand2 = random.randint(24 + ini, 30 + fin - 1)
                # UTILIZO randint porque sample no me deja especificar el rango concreto de numeros, es decir, de 5 a 10 por ejemplo, sino que es un rango tal que range(200)
                while rand1 == rand2:
                    rand2 = random.randint(24 + ini, 30 + fin - 1)
                h1 = chromosome[rand1]
                h2 = chromosome[rand2]
                chromosome[rand2] = h1
                chromosome[rand1] = h2

        ini += 30
        fin += 30


def mutation(chromosome):
    copy = list(chromosome)
    #fitness_old = fitness(copy)
    mutation_hour(copy)
    mutation_day(copy)
    #fitness_new = fitness(copy)
    #if fitness_old < fitness_new:
    #    copy = chromosome
    return copy


def do_mutation(population):
    res = list()
    for chrom in population:
        res.append(mutation(chrom))
    return res


def crosover(ind1, ind2):
    ini = 0
    fin = 0
    child1, child2 = list(), list()
    for num in range(PROFESSOR_NUMBER):  # por cada profesor
        rand_num = range(0, 7)
        j = 0
        i = -1
        while j < 5:  # por cada dia de la semana
            j += 1
            i += 1
            ch1 = ind1[(i * 6 + ini):(j * 6 + fin)]
            ch2 = ind2[(i * 6 + ini):(j * 6 + fin)]
            r1 = random.sample(rand_num, 2)
            r1.sort()

            c1_1 = ch1[r1[0]:r1[1]]  # parte incluida en los pivotes
            c1_i = ch1[0:r1[0]]  # parte excluida a la izquierda de los pivotes
            c1_d = ch1[r1[1]::]  # parte excluida a la derecha de los pivotes

            c2_1 = ch2[r1[0]:r1[1]]  # parte incluida en los pivotes
            c2_i = ch2[:r1[0]]  # parte excluida a la izquierda de los pivotes
            c2_d = ch2[r1[1]::]  # parte excluida a la derecha de los pivotes

            # FORMANDO CHILD 1
            c1_x = list(c1_1)  # lista auxiliar para nuevo hijo
            for elem in ch2:  # vamos metiendo en orden elementos del padre2 en el hijo1 comprobando que no se esten repetidos
                if c1_x.__len__() > 5:
                    break
                elif elem not in c1_1:
                    c1_x.append(elem)

            if c1_x.__len__() < 6:  # caso hipotetico en el que no haya suficientes elementos no repetidos en el padre2 para satisfacer el hijo1
                for elem in ch1:
                    if c1_x.__len__() > 5:
                        break
                    elif elem not in c1_x or elem == 0:
                        c1_x.append(elem)

            # comprobamos que no perdemos ninguna asignatura
            for elem in ch1:
                if elem not in c1_x:
                    if 0 in c1_x:
                        indx = c1_x.index(0)
                        c1_x[indx] = elem
                    else:
                        pass  # TODO creo que este caso no se va a dar nunca

            # extendemos el nuevo hijo con un este nuevo dia de un profesor
            child1.extend(c1_x)

            # FIN CHILD1

            # FORMANDO CHILD 2
            # para el segundo hijo tomamos sus partes excluidas por los pivotes
            # y formaremos nuevo individuo utilizando las partes no repetidas del primer individuo

            c2_x = list(c2_i + c2_d)
            for elem in ch1:
                if c2_x.__len__() > 5:
                    break
                elif elem not in c2_x:
                    c2_x.append(elem)

            if c2_x.__len__() < 6:  # caso hipotetico en el que no haya suficientes elementos no repetidos en el padre1 para satisfacer el hijo2
                for elem in ch2:
                    if c2_x.__len__() > 5:
                        break
                    elif elem not in c2_x or elem == 0:
                        c2_x.append(elem)

            # comprobamos que no perdemos ninguna asignatura
            for elem in ch2:
                if elem not in c2_x:
                    if 0 in c2_x:
                        indx = c2_x.index(0)
                        c2_x[indx] = elem
                    else:
                        pass  # TODO creo que este caso no se va a dar nunca

            child2.extend(c2_x)
            # FIN CHILD 2

            rand_num = range(6 * i, 6 * j)
        ini += 30
        fin += 30
        for elem in child1:
            if elem == 0:
                pass
            else:
                while child1.count(elem) > SUBJECTS_REPETITIONS[elem]:
                    child1[child1.index(elem)] = 0

        for elem in child2:
            if elem == 0:
                pass
            else:
                while child2.count(elem) > SUBJECTS_REPETITIONS[elem]:
                    child2[child2.index(elem)] = 0
                    # TODO comentar en memoria que la anterior comprobacion es computacionalmente inviable!!!!!!

    fitness_old1 = fitness(ind1)
    fitness_old2 = fitness(ind2)
    fitness_new1 = fitness(child1)
    fitness_new2 = fitness(child2)
    if fitness_old1 < fitness_new1:
        child1 = ind1
    if fitness_old2 < fitness_new2:
        child2 = ind2
    


    return child1, child2


def do_crossover(population):
    resu = list()
    len = population.__len__()
    for pos in range(int(len / 2)):
        p1 = random.randint(0, len - 1)

        if p1 == 0 or p1 == 1:
            p2 = random.randint(1, 50)
        else:
            p2 = random.randint(0, p1 - 1)

        c1, c2 = crosover(population[p1], population[p2])
        resu.append(c1)
        resu.append(c2)
    return resu


    # fitness
    """
    1º Ver si un profesor da más asignaturas al día de las permitidas.
            Con que un profesor no lo cumpla ya vale,
            se le da el peor valor a la solución y no hace falta comprobar
            el resto de condiciones. Si das las asignaturas correctas se pasa
            a comprobar las siguientes condiciones.
    2º Ver si un profesor da al mismo curso la misma asignatura más de una vez al día.
    3º Ver si varios profesores dan clase de la misma asignatura el mismo día al mismo curso, a la misma o disinta hora
    """


def checkGroups(individuo):
    res = 0
    for day in range(5):  # 5 dias de la semana
        for hour in range(6):  # 0 al 7, no del 1 al 8
            auxlist = []
            profcounter = 0
            counter = 0
            while counter < PROFESSOR_NUMBER:
                subject = individuo[hour + profcounter]
                if subject == 0:
                    pass
                else:
                    group = subject[-2::]
                    auxlist.append(group)  # funciona con grupos de 2 digitos tipo 2A 3B 4D
                profcounter += 30
                counter += 1
            for elem in auxlist:
                if auxlist.count(elem) > 1:
                    # print('Incompatibilidad de horarios en el grupo ' + elem)
                    res += 1
    return res


def fitness(ind):
    MAXIMUM_HOURS_BY_LAW = 4
    # ###########---------  1  --------------#############
    """1º Ver si un profesor da más asignaturas al día de las permitidas."""
    init = 0
    fin = 39  # 8 h. per day * 5 days

    res = 999
    for i in range(PROFESSOR_NUMBER):

        init_day = 0
        fin_day = 5
        timetable = ind[init:fin]

        for j in range(5):  # 5 dias a la semana
            t = timetable[init_day:fin_day]
            count = 6 - t.count(0)
            if count > MAXIMUM_HOURS_BY_LAW:
                res += 999
                break  # muy ilegal
            else:
                res -= 66  # quita un maximo de 5*66 = 330
            
            if res < 0:
                res = 0

            init_day += 6
            fin_day += 6
        init += 30
        fin += 30
    check = checkGroups(ind)
    if check > 0:
        res += 10 * check
    else:
        res -= 100
    # clock = random.sample(0,PROFESSOR_NUMBER)
    if res < 0:
            res = 0
    return res


# comparator para elite
def cmp_elite(ind1):
    return fitness(ind1)


# seleccion antes del fitness
def selection(pop):
    # tenemos que elegir que porcentaje de la poblacion seleccionamos, y luego de ese porcentaje, cual sera escogido de forma aleatoria y
    # cual sera seleccionado por elite

    l = int(len(pop) * PERC_POP / 100)
    random.shuffle(pop)
    ramdomness = pop[:int(l * PERC_RANDOM / 100)]
    elite = sorted(pop[int(l * PERC_RANDOM / 100):], key=cmp_elite)  # ordenamos para elite
    elite = elite[:int(len(elite) * (100 - PERC_RANDOM) / 100)]
    # print(phenotype(elem))
    # print(fitness(elem))
    return ramdomness + elite  # devolvemos lista conjunta





    # quita var prof
    # cuadra o no cuadra, distinguir dos tipos de individuos, legal o no legal, puntuaciones distintas.
    # Seleccion de padres que mire el fitness
    # sumar res si falla hoursbylaw, dependiendo del numero de horas desfasadas.

    # ## por hacer ###
    # relacion profesores con sus asignaturas -- hecho
    # Fitness version 1: puntuacion legal vs ilegal vs muy ilegal -- hecho
    # Seleccion de padres, y de los que sobreviven segun el fitness. -- hecho
    # cada profesor tiene sus asignaturas que se han repartido antes. -- hecho
    # print el mejor individuo
    # cuantas generaciones quieres. -- hecho
    # # otros parms...
    # # tamano poblacion -- hecho
    # # probabilidad mutacion -- hecho
    # # ... depende de la seleccion que vayamos a elegir.


def prueba(FILENAME):

    asgmnts = initialize(FILENAME)
    count = NUM_GENERATIONS
    res = initPopulation(asgmnts)

    fitness_counter = 0
    old_fitness = 0
    global PROB_MUTATION
    mejoresInd = []
    res = sorted(res, key=cmp_elite)
    f1 = open('media_fitness_por_generacion.txt', 'w')
    while (count > 0):
        print('Generacion ' + str(count))
        print('Aplicando crosover')
        res_n = do_crossover(res)
        print('Mutando con probabilidad ' + str(PROB_MUTATION))
        do_mutation(res_n)
        # print('Seleccionando individuos de la generacion ' + str(count))
        # selected = selection(res_n)

        res_n = sorted(res_n, key=cmp_elite)
        len_aux = int(res.__len__() / 10)
        res = res[:len_aux] + res_n[:-5]  # Nosquedamos con los 5 mejores de la anterior y el resto de la nueva encontrada, así siempre mantenmos las 5 mejores soluciones encontradas
        print('Proceso de seleccion finalizado')
        res = sorted(res, key=cmp_elite)
        fitn = fitness(res[0])
        print('Fitness del mejor individuo de la generacion: ' + str(
            fitn))  # + ' tiene la siguiente forma')
        mejoresInd.append(res[0])
        # print(phenotype(res[0]))
        # print(" El fitness del mejor individuo es " + str(fitness(res[0])))
        if count == NUM_GENERATIONS:
            old_fitness = fitn
        if fitn >= old_fitness:
            fitness_counter += 1
        if fitness_counter > 4 and PROB_MUTATION < 100:
            PROB_MUTATION += 10
            fitness_counter = 0
        aux = 0
        for elem in res:
            aux += fitness(elem)
        aux = aux/res.__len__()
        print('Se pisan ' + str(checkGroups(res[0])) + ' horarios en el mejor individuo')
        print('El fitness medio es ' + str(aux) + ' \n')
        f1.write(str(aux) + '\n')
        if fitn == 0:
            count = 0
        old_fitness = fitn

        count -= 1

    mejoresInd = sorted(mejoresInd, key=cmp_elite)
    print(" El fitness del mejor individuo es " + str(fitness(mejoresInd[0])))
    f1.write('Mejor individuo: ' + str(fitness(mejoresInd[0])))
    f1.close()
    write_sort_res(mejoresInd[0])
    f = open('scheduleByTeacher.txt', 'w')

    print(mejoresInd[0])
    pheno = phenotype(mejoresInd[0])
    for prof, subj in pheno.items():
        #x = open('horarios individuales/' + prof + '.txt', 'w')
        #x.write('Horario del profesor ' + str(prof) + '\n')
        f.write('Horario del profesor ' + str(prof) + '\n')
        for num in range(subj.__len__()):
            if num == 0:
                f.write('###### Lunes ###### \n')
                #x.write('###### Lunes ###### \n')
            if num == 6:
                f.write('###### Martes ###### \n')
                #x.write('###### Martes ###### \n')
            if num == 12:
                f.write('###### Miercoles###### \n')
                #x.write('###### Miercoles###### \n')
            if num == 18:
                f.write('###### Jueves ###### \n')
                #x.write('###### Jueves ###### \n')
            if num == 24:
                f.write('###### Viernes ###### \n')
                #x.write('###### Viernes ###### \n')
            f.write(str(subj[num]) + '\n')
            #x.write(str(subj[num]) + '\n')
            #x.close()

    f.close()

    f = open('scheduleGlobal.txt', 'w')

    incompatibilidades = checkGroups(mejoresInd[0])
    if incompatibilidades == 0:
        print('No se pisan horarios entre grupos')
    else:
        print('Se pisan ' + str(int(incompatibilidades/2)) + ' horarios entre grupos!!!')

def write_sort_res(something):
    monday = something[0::5]
    tuesday = something[1::5]
    wednesday = something[2::5]
    thursday = something[3::5]
    friday = something[4::5]
    f = open('sorted_by_day.txt', 'w')
    f.write(' ## MONDAY ## \n')
    for elem in monday:
        f.write(str(elem) + ' \n')
    f.write(' ## TUESDAY ## \n')
    for elem in tuesday:
        f.write(str(elem) + ' \n')
    f.write(' ## WEDNESDAY ## \n')
    for elem in wednesday:
        f.write(str(elem) + ' \n')
    f.write(' ## THURSDAY ## \n')
    for elem in thursday:
        f.write(str(elem) + ' \n')
    f.write(' ## FRIDAY ## \n')
    for elem in friday:
        f.write(str(elem) + ' \n')
    f.close()






# prueba('assignments.txt')

# print(sorted(initPopulation(),key=cmp_elite))

# print(c1)
# print(len(c1))
# print(c2)
# print(len(c2))


# ###### GUI #######

ROOT = tk.Tk()

def run_algorithm():
    file = filedialog.askopenfilename(initialdir="", title="choose your assignments file")
    #running = tk.Tk()
    #running.title("Working...")
    #running.minsize(10,10)
    #running.geometry("150x150")
    #r = tk.Text(running, height=2,width=100)
    #r.insert(tk.END," Please, grab a coffe or two while we are working ")
    #r.pack()

    #r.insert(tk.END, " Please, take a coffe or two while we are working ;)")
    prueba(file)
    #r.insert(tk.END," Your schedule has been generated ! ")

def run_help():
    help = tk.Tk()
    help.title("Help")
    help.minsize(300, 200)
    help.geometry("400x300")
    T = tk.Text(help,height=2,width=30)
    T.pack()
    T.insert(tk.END, "")
    help.mainloop()



def startx():
    # # base window

    ROOT.title("GENHORA")
    ROOT.minsize(300, 200)
    ROOT.geometry("400x300")

    ## to fill rows ##
    #f1 = tk.Frame(ROOT,height=50,width=50)
    #f1.pack_propagate(0) # do not 
    #f1.grid(row=2,column=0)
    #f1.pack()
    #btn_help = tk.Button(ROOT,text="Help", command=run_help)
    #btn_help.pack(side=tk.TOP)
 
    ## to fill rows ##
    f = tk.Frame(ROOT,height=200,width=200)
    f.pack_propagate(0) # do not shrink
    f.grid(row=2,column=1)
    f.pack()
    btn_run = tk.Button(f, text="Generate schedule", command=run_algorithm)
    btn_run.pack(fill=tk.BOTH, expand=1)

    version = tk.Frame(ROOT, height=200, width=200)
    version.pack_propagate(0)
    version.grid(row=3,column=1)
    version.pack()
    version_text = tk.Label(version,text= "BETA v1")
    version_text.pack(fill=tk.BOTH, expand=1, side=tk.BOTTOM)
    
    ROOT.mainloop()

    ## base window


startx()

# ###### END GUI ######








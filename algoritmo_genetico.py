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
# from mpi4py import MPI

# Inicializacion del programa

NUM_GENERATIONS = 50
TAM_POPULATION = 200
PROB_MUTATION = 70
# # atributos metodo selection
PERC_POP = 100
PERC_RANDOM = 20
# # end atributos metodo selection
# # atributos metodo crossover
PERC_POP_CROS = 20
# # end atributos metodo crossover
PARSE_ASSIGNMENTS = defaultdict(set)
SUBJECTS = [0]  # Inicializamos con 0 que representa hora libre
SUBJECTS_REPETITIONS = defaultdict(int)
PROFESSORS = []
ASSIGNMENTS = fileparser.read_assignments()  # Cargamos los datos de inicio desde un archivo .txt utilizando un archivo python externo
# Variables que guardaran la informacion recogida del archivo .txt, incicializandolas 0
SUBJECTS_NUMBER = 0
PROFESSOR_NUMBER = 0
n = 0
pos = 1
subjs = []
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
                        subj[0:-1] + ' ' + subj[-1])  # obtenemos nombre de cada asignatura
            res.update({professor: prof_subj})
    return res

    # # end help methods for phenotype


def inputData():
    professor_number = int(input("Introduzca el número de profesores"))

    return professor_number


def initIndividual():
    """ Generates random data for the individual solution """
    #MAXIMUM_HOURS_BY_LAW = 3  # Numero maximo de asignaturas que puede, por ley, impartir un profesor por dia
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
        monday += (8 - monday.__len__()) * zeros
        random.shuffle(monday)

        for n in range(4):
            if aux.__len__() > 0:
                if aux[0] not in tuesday:
                    tuesday.append(aux.pop(0))
        tuesday += (8 - tuesday.__len__()) * zeros
        random.shuffle(tuesday)

        for n in range(4):
            if aux.__len__() > 0:
                if aux[0] not in wednesday:
                    wednesday.append(aux.pop(0))
        wednesday += (8 - wednesday.__len__()) * zeros
        random.shuffle(wednesday)

        for n in range(4):
            if aux.__len__() > 0:
                if aux[0] not in thursday:
                    thursday.append(aux.pop(0))
        thursday += (8 - thursday.__len__()) * zeros
        random.shuffle(thursday)

        for n in range(4):
            if aux.__len__() > 0:
                if aux[0] not in friday:
                    friday.append(aux.pop(0))
        friday += (8 - friday.__len__()) * zeros
        random.shuffle(friday)

        ind += monday + tuesday + wednesday + thursday + friday

    return ind


def phenotype(genotype):
    BY_PROFESSOR = list()
    BY_DAY_PROFESSOR = list()
    PROFESSOR_WEEK = dict()
    for num in range(PROFESSOR_NUMBER):
        fin = (num + 1) * 40  # TODO aqui se ha tomado 8 como numero de asignaturas
        ini = num * 40
        BY_PROFESSOR.append(genotype[ini:fin])
    count = 0
    for prof in BY_PROFESSOR:
        BY_DAY_PROFESSOR.append(prof[:8])
        BY_DAY_PROFESSOR.append(prof[8:16])
        BY_DAY_PROFESSOR.append(prof[16:24])
        BY_DAY_PROFESSOR.append(prof[24:32])
        BY_DAY_PROFESSOR.append(prof[32:40])
        PROFESSOR_WEEK.update({count: BY_DAY_PROFESSOR})
        BY_DAY_PROFESSOR = list()
        count = count + 1
    return parse_professor(PROFESSOR_WEEK)


def initPopulation():
    return [initIndividual() for _ in range(TAM_POPULATION)]


def mutation(chromosome):
    """
    :param chromosome: entrada a modificar
    :return: cromosoma mutado o sin mutar
    """
    # TODO mismo profesor
    # TODO probabilidad
    """checkprob = random.randint(0, 100)
    if checkprob <= PROB_MUTATION:
        p1 = random.randint(0, len(chromosome) - 1)
        p2 = random.randint(0, len(chromosome) - 1)
        while p2 == p1:
            p1 = random.randint(0, len(chromosome) - 1)
        if not p1 == 0 or p2 == 0:
            a = chromosome[p1]
            b = chromosome[p2]
            chromosome[p1] = b
            chromosome[p2] = a
            return chromosome
    else:        
        return chromosome"""

    ini = 0
    fin = 0
    for prof in range(PROFESSOR_NUMBER):
        for i in range(0 + ini, 8 + fin - 1):

            checkprob = random.randint(0, 100)
            if checkprob <= PROB_MUTATION:
                rand1 = random.randint(0 + ini, 8 + fin - 1)
                rand2 = random.randint(0 + ini, 8 + fin - 1)
                # UTILIZO randint porque sample no me deja especificar el rango concreto de numeros, es decir, de 5 a 10 por ejemplo, sino que es un rango tal que range(200)
                while rand1 == rand2:
                    rand2 = random.randint(0 + ini, 8 + fin - 1)
                h1 = chromosome[rand1]
                h2 = chromosome[rand2]
                chromosome[rand2] = h1
                chromosome[rand1] = h2
                # Se intercambian horas del mismo dia

        for i in range(8 + ini, 16 + fin - 1):

            checkprob = random.randint(0, 100)
            if checkprob <= PROB_MUTATION:
                rand1 = random.randint(8 + ini, 16 + fin - 1)
                rand2 = random.randint(8 + ini, 16 + fin - 1)
                # UTILIZO randint porque sample no me deja especificar el rango concreto de numeros, es decir, de 5 a 10 por ejemplo, sino que es un rango tal que range(200)
                while rand1 == rand2:
                    rand2 = random.randint(8 + ini, 16 + fin - 1)
                h1 = chromosome[rand1]
                h2 = chromosome[rand2]
                chromosome[rand2] = h1
                chromosome[rand1] = h2

        for i in range(16 + ini, 24 + fin - 1):

            checkprob = random.randint(0, 100)
            if checkprob <= PROB_MUTATION:
                rand1 = random.randint(16 + ini, 24 + fin - 1)
                rand2 = random.randint(16 + ini, 24 + fin - 1)
                # UTILIZO randint porque sample no me deja especificar el rango concreto de numeros, es decir, de 5 a 10 por ejemplo, sino que es un rango tal que range(200)
                while rand1 == rand2:
                    rand2 = random.randint(16 + ini, 24 + fin)
                h1 = chromosome[rand1]
                h2 = chromosome[rand2]
                chromosome[rand2] = h1
                chromosome[rand1] = h2

        for i in range(24 + ini, 32 + fin - 1):

            checkprob = random.randint(0, 100)
            if checkprob <= PROB_MUTATION:
                rand1 = random.randint(24 + ini, 32 + fin - 1)
                rand2 = random.randint(24 + ini, 32 + fin - 1)
                # UTILIZO randint porque sample no me deja especificar el rango concreto de numeros, es decir, de 5 a 10 por ejemplo, sino que es un rango tal que range(200)
                while rand1 == rand2:
                    rand2 = random.randint(24 + ini, 32 + fin)
                h1 = chromosome[rand1]
                h2 = chromosome[rand2]
                chromosome[rand2] = h1
                chromosome[rand1] = h2

        for i in range(32 + ini, 40 + fin - 1):

            checkprob = random.randint(0, 100)
            if checkprob <= PROB_MUTATION:
                rand1 = random.randint(32 + ini, 40 + fin - 1)
                rand2 = random.randint(32 + ini, 40 + fin - 1)
                # UTILIZO randint porque sample no me deja especificar el rango concreto de numeros, es decir, de 5 a 10 por ejemplo, sino que es un rango tal que range(200)
                while rand1 == rand2:
                    rand2 = random.randint(32 + ini, 40 + fin - 1)
                h1 = chromosome[rand1]
                h2 = chromosome[rand2]
                chromosome[rand2] = h1
                chromosome[rand1] = h2

        ini += 40
        fin += 40
        # Muta en cada elemento excepto si es un 0
        # for i in range(len(chromosome)):
        # checkprob = random.randint(0, 100)
        # if checkprob <= PROB_MUTATION:
        # if not chromosome[i] == 0:
        # chromosome[i] = random.randint(0, SUBJECTS_NUMBER - 1)
    return chromosome


def do_mutation(population):
    res = list()
    for chrom in population:
        res.append(mutation(chrom))
    return res


def crosover(ind1, ind2):
    # r1 = random.randint(1, len(ind1) - 1)
    # r2 = random.randint(1, len(ind1) - 1)
    # r3 = random.randint(1, len(ind1) - 1)
    # r4 = random.randint(1, len(ind1) - 1)

    # Con esto se asegura la unicidad de pivotes sin tener que comprobarlo
    """rand_nums = list(random.sample(range(0, 40 * PROFESSOR_NUMBER),
                                   40 * PROFESSOR_NUMBER))  # 40 --> Franjas horarias * dias semana = datos 1 profesor
    random.shuffle(rand_nums)
    r1 = rand_nums.pop()
    r2 = rand_nums.pop()
    r3 = rand_nums.pop()
    r4 = rand_nums.pop()

    pl = [r1, r2, r3, r4]  # pivotes unicos
    pl.sort()

    ch1_1 = ind1[pl[0]:pl[1]]
    ch1_2 = ind1[pl[2]:pl[3]]
    ch2_1 = ind2[pl[0]:pl[1]]
    ch2_2 = ind2[pl[2]:pl[3]]

    child1 = ind1[:pl[0]] + ch2_1 + ind1[pl[1]:pl[2]] + ch2_2 + ind1[pl[3]:]
    child2 = ind2[:pl[0]] + ch1_1 + ind2[pl[1]:pl[2]] + ch1_2 + ind2[pl[3]:]"""
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
            ch1 = ind1[(i * 8 + ini):(j * 8 + fin)]
            ch2 = ind2[(i * 8 + ini):(j * 8 + fin)]
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
                if c1_x.__len__() > 7:
                    break
                elif elem not in c1_1:
                    c1_x.append(elem)

            if c1_x.__len__() < 8:  # caso hipotetico en el que no haya suficientes elementos no repetidos en el padre2 para satisfacer el hijo1
                for elem in ch1:
                    if c1_x.__len__() > 7:
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
                if c2_x.__len__() > 7:
                    break
                elif elem not in c2_x:
                    c2_x.append(elem)

            if c2_x.__len__() < 8:  # caso hipotetico en el que no haya suficientes elementos no repetidos en el padre1 para satisfacer el hijo2
                for elem in ch2:
                    if c2_x.__len__() > 7:
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
            # c2_1 = ch2[r1[0]:r1[1]]
            # c2_2 = ch2[r1[2]:r1[3]]

            # c1_1 = ch1[r1[0]:r1[1]]
            # c1_2 = ch1[r1[2]:r1[3]]

            # c2_1x = list(c1_1)  # lista provisional para cruce
            # for num in range(c2_1.__len__()):
            # if not c2_1[num] in ch1:  # TODO no se mantienen las horas en su sitio
            # c2_1x[num] = c2_1[
            # num]  # si la asignatura no esta repetida, entonces la introducimos en el nuevo hijo, en caso contrario mantiene asignacion de padre.
            #
            # c2_2x = list(c1_2)
            # for num in range(c2_2.__len__()):
            #     if not c2_2[num] in ch1:  # TODO no se mantienen las horas en su sitio
            #         c2_2x[num] = c2_2[num]
            #
            # c1_1x = list(c2_1)
            # for num in range(c1_1.__len__()):
            #     if not c1_1[num] in ch2:  # TODO no se mantienen las horas en su sitio
            #         c1_1x[num] = c1_1[num]
            #
            # c1_2x = list(c2_2)
            # for num in range(c1_2.__len__()):
            #     if not c1_2[num] in ch2:  # TODO no se mantienen las horas en su sitio
            #         c1_2x[num] = c1_2[num]
            #
            # child1.extend(ch1[:r1[0]] + c2_1x + ch1[r1[1]:r1[2]] + c2_2x + ch1[r1[3]:])
            # child2.extend(ch2[:r1[0]] + c1_1x + ch2[r1[1]:r1[2]] + c1_2x + ch2[r1[3]:])

            rand_num = range(8 * i, 8 * j)
        ini += 40
        fin += 40
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



    return child1, child2


def do_crossover(population):
    res = list()
    len = population.__len__()
    for pos in range(int(len / 2)):
        p1 = random.randint(0, len - 1)

        if p1 == 0 or p1 == 1:
            p2 = random.randint(1, 50)
        else:
            p2 = random.randint(0, p1 - 1)

        c1, c2 = crosover(population[p1], population[p2])
        res.append(c1)
        res.append(c2)
    return res


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


def fitness(ind):
    MAXIMUM_HOURS_BY_LAW = 4
    # ###########---------  1  --------------#############
    """1º Ver si un profesor da más asignaturas al día de las permitidas."""
    init = 0
    fin = 39  # 8 h. per day * 5 days

    res = 999
    for i in range(PROFESSOR_NUMBER):

        init_day = 0
        fin_day = 7
        timetable = ind[init:fin]

        for j in range(5):  # 5 dias a la semana
            t = timetable[init_day:fin_day]
            count = 8 - t.count(0)
            if count > MAXIMUM_HOURS_BY_LAW:
                res += 999
                break  # muy ilegal
            else:
                res -= 66  # quita un maximo de 5*66 = 330

            init_day += 8
            fin_day += 8

        if res < 0:
            res = 0
        init += 40
        fin += 40
    #clock = random.sample(0,PROFESSOR_NUMBER)
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


def prueba():
    # COMM=MPI.COMM_WORLD
    # SIZE=COMM.Get_size() #Get number of proceses
    # RANK=COMM.Get_rank() #Get id of own process
    count = NUM_GENERATIONS
    res = initPopulation()
    # print(" El fitness del mejor individuo es " + str(fitness(res[0])))

    mejoresInd = []
    res = sorted(res, key=cmp_elite)

    while (count > 0):
        print('Aplicando crosover en generacion ' + str(count))
        res_n = do_crossover(res)
        print('Mutando generacion ' + str(count))
        do_mutation(res_n)
        # print('Seleccionando individuos de la generacion ' + str(count))
        # selected = selection(res_n)

        res_n = sorted(res_n, key=cmp_elite)
        res = res[:5] + res_n[
                        :95]  # Nosquedamos con los 5 mejores de la anterior y el resto de la nueva encontrada, así siempre mantenmos las 5 mejores soluciones encontradas
        print('Proceso de seleccion de la generacion ' + str(count) + ' finalizado')
        res = sorted(res, key=cmp_elite)
        print('El mejor individuo encontrado en generacion ' + str(count) + ' con fitness ' + str(fitness(
            res[0])))  # + ' tiene la siguiente forma')
        mejoresInd.append(res[0])
        # print(phenotype(res[0]))
        # print(" El fitness del mejor individuo es " + str(fitness(res[0])))

        """Para el modelo paralelo en islas,
            cada Isla será una ejecución del algoritmo,
            entre islas se comparten individuos(los X mejores individuos se envian) y 
            los que recibimos se sustituyen por los X peores de la propia población.
            Ahora se comunican en anillo procesos: 0->1->2->3->0"""

        """d=(RANK+1)%SIZE
        s=(RANK-1+SIZE)%SIZE
        #Enviamos los 10 mejores        
        indrecv=COMM.sendrecv(res[:10],dest=d,source=s,sendtag=1,recvtag=1)
        COMM.Barrier() #Barerra de sincronización
        #Sustituyo por los 10 peores
        res=res[:TAM_POPULATION-10]+indrecv"""
        count -= 1

    mejoresInd = sorted(mejoresInd, key=cmp_elite)
    print(" El fitness del mejor individuo es " + str(fitness(mejoresInd[0])))
    # print(phenotype(mejoresInd[0]))
    pheno = phenotype(mejoresInd[0])
    for prof, subj in pheno.items():
        print('Horario del profesor ' + str(prof))
        for num in range(subj.__len__()):
            if num == 0:
                print('###### Lunes ######')
            if num == 8:
                print('###### Martes ######')
            if num == 16:
                print('###### Miercoles######')
            if num == 24:
                print('###### Jueves ######')
            if num == 32:
                print('###### Viernes ######')
            print(str(subj[num]))


prueba()
#print(sorted(initPopulation(),key=cmp_elite))

# print(c1)
# print(len(c1))
# print(c2)
# print(len(c2))











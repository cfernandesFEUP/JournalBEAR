## IMPORTAÇÃO DAS LIBRARIAS ###################################################

import numpy as np

from scipy import interpolate

import matplotlib.pyplot as plt

import lubricants as lub

import tables as tab

import sys

## DADOS CHUMACEIRA ###########################################################

# Comprimento / m
L = float(input("Comprimento da chumaceira L / mm: "))/1000

# Diâmetro / m
D = float(input("Diâmetro da chumaceira D / mm: "))/1000

# Folga radial / m
c = float(input("Folga radial c / \u03BCm: "))/1000000

## CONDIÇÕES DE FUNCIONAMENTO #################################################

lubrificante = input("Lubrificante: ")

# Carga / N
W = float(input("Carga W / N: "))

# Velocidade angular do veio / rpm
N = float(input("Velocidade angular da chumaceira N / rpm: "))

# Temperatura de alimentação / ºC
T0 = float(input(u"Temperatura de alimentação do lubrificante T0 / \u00b0C: "))

alpha = 0.8

## LEI ASTM ###################################################################
base, m, n, alphaT, rho, cp = lub.oil(lubrificante)


def ASTM(T, m, n):
    return -0.7 + 10**(10**(m - n*np.log10(T+273.15)))


def CRHsolver(L, D, c, N, W, eta, rho, cp, alpha, T0, ITER):
    ## NÚMERO DE SOMMERFELD #######################################################
    # Velocidade linear do veio / m/s
    V = np.pi*N*D/60

    S = (eta*L*V/(np.pi*W))*(D/(2*c))**2

    if 0.001 < S > 17:
        sys.exit('Sem solução para as condições de funcionamento escolhidas.')

## PARÂMETROS DE FUNCIONAMENTO DA CHUMACEIRA ##################################

    LD = L/D

    fepsilon = interpolate.interp1d(tab.DIC[LD]['S'], tab.DIC[LD]['eps'])

    fphi = interpolate.interp1d(tab.DIC[LD]['S'], tab.DIC[LD]['phi'])

    ffa = interpolate.interp1d(tab.DIC[LD]['S'], tab.DIC[LD]['Rcfa'])

    fQa = interpolate.interp1d(tab.DIC[LD]['S'], tab.DIC[LD]['QLcV'])

    epsilon = fepsilon(S)

    hmin = c*(1 - epsilon)

    hmicron = 1e6*hmin

    phi = fphi(S)

    fa = ffa(S)*2*c/D

    Ca = fa*D*W/2

    Qa = fQa(S)*L*c*V
    Qal = 60000*Qa

    Qc = hmin*L*V/2
    Qcl = 60000*Qc

    Pa = Ca*np.pi*N/30

## CÁLCULO DA TEMPERATURA NO DIVERGENTE #######################################

    T2 = T0 + alpha*Pa*(Qa + Qc)/(rho*cp*Qa*(Qa/2 + Qc))

## CÁLCULO DA TEMPERATURA QUE SAI PELOS BORDOS ################################

    Te = (T0*Qa + T2*Qc)/(Qa + Qc)

## CÁLCULO DA TEMPERATURA DO FILME ############################################

    Ti = (Te + T2)/2

    dash = '-' * 65
    dots = '.' * 65

    print(dash)
    print('ITERAÇÃO Nº', ITER)
    print(dots)
    print('Viscosidade dinâmica [mPas]', "%.4f" % eta)
    print('Velocidade linear [m/s]', "%.2f" % V)
    print('Número de Sommerfeld [-]', "%.4f" % S)
    print('Excentricidade relativa [-]', "%.2f" % epsilon)
    print('Espessura de filme mínima [\u03BCm]', "%.3f" % hmicron)
    print(u'Ângulo de posicionamento [\u00b0]', "%.2f" % phi)
    print('Coeficiente de atrito [-]', "%.4f" % fa)
    print(u'Caudal no convergente [l/min]', "%.3f" % Qcl)
    print(u'Caudal de alimentação [l/min]', "%.3f" % Qal)
    print('Momento de atrito [Nm]', "%.2f" % Ca)
    print('Potência de Atrito [W]', "%.2f" % Pa)
    print(u'Temperatura de alimentação [\u00b0C]', "%.2f" % T0)
    print(
        u'Temperatura do lubrificante que sai pelos bordos [\u00b0C]', "%.2f" % Te)
    print(u'Temperatura média do filme [\u00b0C]', "%.2f" % Ti)
    print(u'Temperatura do lubrificante no divergente [\u00b0C]', "%.2f" % T2)
    print(dash)

    return V, Te, Ti, T2, S, epsilon, hmin, phi, fa, Ca, Qal, Qcl, Pa, LD

## VISCOSIDADE CINEMÁTICA E DINÂMICA ##########################################


Tfilme = T0

delta = 1

ITERS, ITERT, ITERD = [], [], []

ITER = 1

while delta >= 0.05:

    ITERS.append(ITER)
    ITERT.append(Tfilme)
    ITERD.append(delta)

    niu = ASTM(Tfilme, m, n)

    eta = niu*rho/1e6

    V, Te, Ti, T2, S, epsilon, hmicron, phi, fa, Ca, Qal, Qcl, Pa, LD\
        = CRHsolver(L, D, c, N, W, eta, rho, cp, alpha, T0, ITER)

    delta = 100*abs(Ti-Tfilme)/Tfilme

    Tfilme = (Ti + Tfilme)/2

    if Tfilme > 100:
        Tfilme = 100

    ITER = ITER + 1

## PLOT #######################################################################

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(ITERS, ITERT, 'k-')
ax2.plot(ITERS, ITERD, 'r-')
ax1.set_xlabel('Nº Iteração')
ax1.set_ylabel(u'$T_i$ / \u00b0C')
ax2.set_ylabel('Erro %', color='r')
plt.grid()
plt.show()

## RESULTADOS #################################################################

dash = '-' * 65
dots = '.' * 65
print(dash)
print('RESULTADO FINAL')
print(dots)
print('Viscosidade dinâmica [mPas]', "%.4f" % eta)
print('Velocidade linear [m/s]', "%.2f" % V)
print('Número de Sommerfeld [-]', "%.4f" % S)
print('Excentricidade relativa [-]', "%.2f" % epsilon)
print('Espessura de filme mínima [\u03BCm]', "%.3f" % hmicron)
print(u'Ângulo de posicionamento [\u00b0]', "%.2f" % phi)
print('Coeficiente de atrito [-]', "%.4f" % fa)
print(u'Caudal no convergente [l/min]', "%.3f" % Qcl)
print(u'Caudal de alimentação [l/min]', "%.3f" % Qal)
print('Momento de atrito [Nm]', "%.2f" % Ca)
print('Potência de Atrito [W]', "%.2f" % Pa)
print(u'Temperatura de alimentação [\u00b0C]', "%.2f" % T0)
print(
    u'Temperatura do lubrificante que sai pelos bordos [\u00b0C]', "%.2f" % Te)
print(u'Temperatura média do filme [\u00b0C]', "%.2f" % Ti)
print(u'Temperatura do lubrificante no divergente [\u00b0C]', "%.2f" % T2)
print(dash)
input('Prima uma tecla para continuar')

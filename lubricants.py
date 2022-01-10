## LIBRARIA DE LUBRIFICANTES ######################################################
def oil(lubrificante):
    if lubrificante == 'MINR':
        base = 'MIN'
        m_astm = 9.0658
        n_astm = 3.4730
        alphaT = -5.8e-4
        roh = 902
        cp = 2306.93
    elif lubrificante == 'MINE':
        base = 'PAO'
        m_astm = 7.0478
        n_astm = 2.6635
        alphaT = -6.97e-4
        roh = 893
        cp = 2306.93
    elif lubrificante == 'PAOR':
        base = 'PAO'
        m_astm = 7.3514
        n_astm = 2.7865
        alphaT = -5.5e-4
        roh = 859
        cp = 2306.93
    elif lubrificante == 'ESTF':
        base = 'EST'
        m_astm = 7.2610
        n_astm = 2.7493
        alphaT = -6.7e-4
        roh = 957
        cp = 2306.93
    elif lubrificante == 'ESTR':
        base = 'EST'           
        m_astm = 7.5823
        n_astm = 2.8802
        alphaT = -8.1e-4
        roh = 915
        cp = 2306.93
    elif lubrificante == 'PAGD':
        base = 'PAG'
        m_astm = 5.7597
        n_astm = 2.1512
        alphaT = -7.1e-4
        roh = 1059
        cp = 2306.93
    elif lubrificante == 'P150':
        base = 'PAO'
        m_astm = 7.646383
        n_astm = 2.928541
        alphaT = -5.5e-4
        roh = 849
        cp = 2306.93
    elif lubrificante == 'FVA3':
        base = 'MIN'
        m_astm = 9.2384
        n_astm = 3.5810
        alphaT = -5.5e-4
        roh = 900
        cp = 2000
    elif lubrificante == 'dry':
        base = 'PAO'
        m_astm = 7.646383
        n_astm = 2.928541
        alphaT = -5.5e-4
        roh = 849
        cp = 2306.93
    elif lubrificante == 'SAE20':
        base = 'MIN'
        m_astm = 8.78117
        n_astm = 3.39785
        alphaT = -5.5e-4
        roh = 875
        cp = 2306.93
    elif lubrificante == '46':
        base = 'MIN'
        m_astm = 10.3095555 
        n_astm = 4.0487591
        alphaT = -5.5e-4
        roh = 875
        cp = 2000
    elif lubrificante == '32':
        base = 'MIN'
        m_astm = 10.52041246
        n_astm = 4.15123574
        alphaT = -5.5e-4
        roh = 875
        cp = 2000
    elif lubrificante == '100':
        base = 'MIN'
        n_astm = 3.80028332
        m_astm = 9.77293932
        alphaT = -5.5e-4
        roh = 875
        cp = 2000
    return base, m_astm, n_astm, alphaT, roh, cp


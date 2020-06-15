# -*- coding: utf-8 -*-
#ADICIONAR path_to_bin NA FUNÇÃO run ANTES DE USAR


## Recebe nome do arquivo e passa pro QE rodar. Por default, utiliza o executável pw.x e dois processadores.
#Argumentos opcionais:
#(1) exe(string): caso o executável chamado não seja o pw.x, especificar (ex: exe='ph.x');
#(2) nprocs(float ou int) Caso não se deseje usar um único processador, especificar (Ex: nproc=1).
#Ex: run('ag.bands.in', nproc=1, exe='bands.x')
def run(filename, **kwargs):
    from os import system
    path_to_bin = '../QE/bin/' #adicionar em cada PC 
    if filename.endswith('.in'):
        filename = filename[:-3]    
    exe = kwargs.get('exe')
    nproc = kwargs.get('nproc')
    cmd = 'mpirun -np 2 '+ path_to_bin + 'pw.x'  +' < ' + filename + '.in > ' + filename + '.out'
    if exe and not nproc:
        cmd = 'mpirun -np 2 '+ path_to_bin + exe + ' < ' + filename + '.in > ' + filename + '.out'
    if nproc and not exe:
        cmd = 'mpirun -np ' + str(nproc)+ ' ' + path_to_bin +'pw.x < ' + filename + '.in > ' + filename + '.out'
    if nproc and exe:
        cmd = 'mpirun -np ' + str(nproc)+ ' ' + path_to_bin + exe + ' < ' + filename + '.in > ' + filename + '.out'          
    return system(cmd)



#coleta a energia do arquivo de saída e converte para eV, dado o nome do arquivo (''). OBS: retorna a energia, mas não necessariamente printa. Ex: E = collect_totE('pt.cubic.out')
def collect_totE(filename):
    infile = open(filename, 'r')
    text = infile.read()
    lines = text.splitlines()
    if '!' in text:
        for line in lines:
            if '!' in line:
                energy = float(line.split()[4]) * 13.6056980659
    else:
        energy = float('NaN')
    infile.close()
    return energy

# EM CONSTRUÇÃO
#def collect_Efermi(filename):

# Altera um parâmetro no arquivo 'filename'.
#Só funciona se o argumento a se alterar estiver sozinho na linha
#Argumentos: param(string), param_value(string, float ou int).
#Exemplo: chg_param('pt.cubic.in', param='nat', param_value=3) altera a variável nat para o valor 3 no arquivo pt.cubic.in
def chg_param(filename, param, param_value):
    infile = open(filename, 'rt')
    text = infile.readlines()
    i = 0
    for line in text:
        if param in line:
            i = text.index(line)
            line_i = text[i].split()
            if type(param_value) != str:
                line_i[2] = str(param_value)
            text[i] = '\t' + ' '.join(line_i) + '\n'
    text = ''.join(text)
    infile.close()
    infile = open(filename, 'wt')
    infile.write(text)
    infile.close()

#altera pontos k do arquivo filename para string fornecida.
#Ex: chg_kpoints(filename, '8 8 8 0 0 0')
def chg_kpoints(filename, X):
    infile = open(filename, 'rt')
    text = infile.readlines()
    for line in text:
        if  'K_POINTS' in line:
            i = text.index(line)
    text[i+1] = X
    text = ''.join(text)
    infile.close()
    infile = open(filename, 'wt')
    infile.write(text)
    infile.close()
    
## Recebe o arquivo .dat de saída do cálculo da DOS ou pDOS e gera um csv, com o mesmo nome, por padrão.
# Se utilizado com o arquivo de saída da DOS, usar o argumento "header". A energia de Fermi não aparecerá no arquivo de saída.
# Obs: se não funcionar, provavelmente é erro de leitura na primeira linha. A primeira linha é printada, para verificação. Se estiver errada, adicionar manualmente com o argumento 'header'.
#Argumento opcional: fileout = nome do arquivo de saída. Ex: dos_dat_to_csv('entrada.dat','fileout='saida.csv')
#Argumento opcional: header = adicionar nome das colunas manualmente (lista de strings). Ex: dos_dat_to_csv('entrada.dat',header=['E (eV)', 'pdos (E)'])
def dos_dat_to_csv(filename, **kwargs):

    fileout = kwargs.get('fileout')
    header = kwargs.get('header')
    if not fileout:
        fileout=filename +'.csv'
    infile = open(filename, 'rt')
    lines = infile.readlines()
    
    #tentativa de construção automatica da primeira linha
    if '\n' in lines[0]:
        lines[0]=lines[0].strip()
    if '#' in lines[0]:
        lines[0]=lines[0].strip('#')
    lines[0]=lines[0].split('   ')
    print(lines[0])
    
    #transformação de dados em floats
    for i in range(1,len(lines)):
        lines[i] = lines[i].split()
        for j in range(0,len(lines[i])):
            lines[i][j]=float(lines[i][j])
            
    #escreve no arquivo de saída
    from pandas import DataFrame
    if not header:
        header = lines[0]
    data = lines[1:len(lines)]
    lines=DataFrame(data, columns=header)
    lines.to_csv(fileout, index=False)

# Transforma arquivo de saída .dat de bandas para arquivo em csv, com formatação mais adequada.
# Argumentos: filename=nome do arquivo de entrada, nbands=quantidade de bandas no arquivo de saída (tem na primeira linha do arquivo .dat)
# Argumento opcional: fileout=nome do arquivo de saída. Ex: fileout='pt.bands.csv'
def bands_dat_to_csv(filename, nbands, **kwargs):
    import numpy as np
    from pandas import DataFrame

    fileout = kwargs.get('fileout')
    if not fileout:
        fileout = filename +'.csv'
    infile = open(filename, 'rt')
    lines = infile.readlines()
    data = lines[1:len(lines)]
    aux = []
    for line in data:
        if '\n' in line:
            line = line.strip('\n')
        line = line.split()
        aux += line
    data=[]
    for item in aux:
        data.append(float(item))
    data = np.array(data)
    data = data.reshape(int(len(data)/(nbands+3)), nbands+3)
    bands = []
    for i in range(1,nbands+1):
        bands.append('band'+str(i))
    header = ['xpos','ypos','zpos']+bands
    data  = DataFrame(data, columns=header)
    data.to_csv(fileout)

##EM CONSTRUÇÃO        
#altera atomic positions do arquivo filename para lista A especificada
#def chg_apos(filename, A):


# Faz um teste de convergência para um parâmetro do tipo parametro=value (o parâmetro tem que estar sozinho na linha do arquivo scf).
# Argumentos:
# filein: nome do arquivo scf. Ex: filein = 'niti.scf.in'
# fileout: nome do arquivo csv gerado. Ex: fileout = 'resultados_convergencia.csv'
# param: parâmetro a se testar. Ex: param='ecutwfc'
# seq: lista com valores a se testar. Ex: seq = [30, 40, 50]
# Argumento opcional: nproc=nº de processadores utilizados na função run
# OBS: a função run envolvida nesse teste salva o arquivo de saída do scf com o mesmo nome do de entrada
def conv_test_param(filein, fileout,param, seq, **kwargs):
    if filein.endswith('.in'):
        scfout = filein[:-3]+'.out'
    nproc_ = kwargs.get('nproc')
    #loop para calcular as energias
    tot_energy= []
    for item in seq:
        chg_param(filein,param,item)
        if nproc_:
            run(filein, nproc=nproc_)
        else:
            run(filein)
        tot_energy += [collect_totE(scfout)]
    #escreve os resultados em um csv:
    from csv import writer
    with open(fileout,'w') as output:
        w = writer(output)
        w.writerow([param, 'Total Energy [eV]']) #escreve o header para o arquivo de saída
        for i in range(len(seq)):
            w.writerow([seq[i],tot_energy[i]])
            
# Faz um teste de convergência para os k-points
# Argumentos:
# filein: nome do arquivo scf. Ex: filein = 'niti.scf.in'
# fileout: nome do arquivo csv gerado. Ex: fileout = 'resultados_convergencia.csv'
# seq: lista com valores a se testar. Ex: seq = ['3 3 3 0 0 0', '4 4 4 0 0 0', '5 5 5 0 0 0']
# OBS: a função run envolvida nesse teste salva o arquivo de saída do scf com o mesmo nome do de entrada
def conv_kpoints(filein, fileout,seq):
    if filein.endswith('.in'):
        scfout = filein.strip('.in')+'.out'
    #loop para calcular as energias
    tot_energy= []
    for kpoint in seq:
        chg_kpoints(filein,kpoint)
        run(filein)
        tot_energy += [collect_totE(scfout)]
        print(tot_energy)
    #escreve os resultados em um csv:
    from csv import writer
    with open(fileout,'w') as output:
        w = writer(output)
        w.writerow(['kpoints', 'Total Energy [eV]']) #escreve o header para o arquivo de saída
        for i in range(len(seq)):
            w.writerow([seq[i],tot_energy[i]])

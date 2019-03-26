str = open('test.txt').read()
line1, output, *_ = str.split('\n', 2)
line1 = line1.split()
rna, trf = output.split('&', 1)
trf = trf[::-1]

symbol_left, symbol_right = line1[0].split('&', 1)
symbol_right = symbol_right[::-1]
rna_start, rna_end = line1[1].split(',', 1)
trf_start, trf_end = line1[3].split(',', 1)

new_trf = ''
j = 0
for i in range(len(symbol_left)):
    if symbol_left[i] == '.' and symbol_right[j] != '.':
        new_trf += '-'
        continue
    if symbol_left[i] == '(':
        new_trf += trf[j]
    if symbol_left[i] == '.' and symbol_right[j] == '.':
        new_trf += '|'
    j += 1


open('output.txt', 'w').write(rna + '\n' + new_trf)

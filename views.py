from pyramid.view import view_config
import subprocess

@view_config(route_name='json', renderer='json')
def get_json(request):
    myData = dict(request.POST.items())
    start = int(myData['start-range'])
    end = int(myData['end-range'])
    rna = myData['RNA'][start-1:end]
    trf = myData['tRF']
    if len(rna) < len(trf):
        tmp = rna 
        rna = trf 
        trf = tmp
    guessed_len = end - start + 1
    origin = rna + '\n' + trf
    RNAup_input = rna + '&' + trf
    
    rna = rna.replace('T', 'U')
    trf = trf.replace('T', 'U')
    t_to_u = rna + '\n' + trf
    
    reverse_trf = rna + '\n' + trf[::-1]

    open('rna-input.txt', 'w').write(RNAup_input)
    # Run RNAup, get test.txt 
    with open('rna-output.txt', 'w') as ouf:
        with open('rna-input.txt', 'r') as inf:
            proc = subprocess.Popen(
                ["RNAup", '-b', '-d2', '--noLP', '-c', 'S'], stdout=ouf, stdin=inf)
            proc.wait()
    str = open('rna-output.txt').read()

    line1, output, *_ = str.split('\n', 2)
    line1 = line1.split()
    rna, trf = output.split('&', 1)
    trf = trf[::-1]

    symbol_left, symbol_right = line1[0].split('&', 1)
    symbol_right = symbol_right[::-1]
    rna_start, rna_end = line1[1].split(',', 1)
    rna_start = int(rna_start)
    rna_end = int(rna_end)
    trf_start, trf_end = line1[3].split(',', 1)
    trf_start = int(trf_start)
    trf_end = int(trf_end)
    matched_len = rna_end - rna_start + 1

    postfix_xcnt = guessed_len - rna_end
    prefix_xcnt = rna_start - 1

    new_trf = ''
    j = 0
    for i in range(len(symbol_left)):
        if symbol_left[i] == '.' and symbol_right[j] != '.':
            new_trf += 'X'
            continue
        if symbol_left[i] == '(':
            new_trf += trf[j]
        if symbol_left[i] == '.' and symbol_right[j] == '.':
            new_trf += 'O'
        j += 1
    for i in range(prefix_xcnt):
        rna = '＃' + rna
        new_trf = '＃' + new_trf

    for i in range(postfix_xcnt):
        rna += '＃'
        new_trf += '＃'

    rnaup_result = rna + '\n' + new_trf

    print(start, end, rna, trf)
    
    ret_dic = {
        'guessed-len': guessed_len,
        'matched-len': matched_len,
        'origin': origin,
        't-to-u': t_to_u,
        'reverse-trf': reverse_trf,
        'rnaup-result': rnaup_result
    }
    
    return ret_dic 

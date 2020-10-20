"""color for cli usage."""
__author__ = 'mangalbhaskar'
nocolor='\033[0m'    ## text reset

###-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## regular                bold                      underline                high intensity             boldhigh intens           background                high intensity backgrounds
###-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
bla,     bbla,     ubla,     ibla,     bibla,     on_bla,     on_ibla = '\033[0;30m',     '\033[1;30m',     '\033[4;30m',     '\033[0;90m',     '\033[1;90m',     '\033[40m',     '\033[0;100m'
red,     bred,     ured,     ired,     bired,     on_red,     on_ired = '\033[0;31m',     '\033[1;31m',     '\033[4;31m',     '\033[0;91m',     '\033[1;91m',     '\033[41m',     '\033[0;101m'
gre,     bgre,     ugre,     igre,     bigre,     on_gre,     on_igre = '\033[0;32m',     '\033[1;32m',     '\033[4;32m',     '\033[0;92m',     '\033[1;92m',     '\033[42m',     '\033[0;102m'
yel,     byel,     uyel,     iyel,     biyel,     on_yel,     on_iyel = '\033[0;33m',     '\033[1;33m',     '\033[4;33m',     '\033[0;93m',     '\033[1;93m',     '\033[43m',     '\033[0;103m'
blu,     bblu,     ublu,     iblu,     biblu,     on_blu,     on_iblu = '\033[0;34m',     '\033[1;34m',     '\033[4;34m',     '\033[0;94m',     '\033[1;94m',     '\033[44m',     '\033[0;104m'
pur,     bpur,     upur,     ipur,     bipur,     on_pur,     on_ipur = '\033[0;35m',     '\033[1;35m',     '\033[4;35m',     '\033[0;95m',     '\033[1;95m',     '\033[45m',     '\033[0;105m'
cya,     bcya,     ucya,     icya,     bicya,     on_cya,     on_icya = '\033[0;36m',     '\033[1;36m',     '\033[4;36m',     '\033[0;96m',     '\033[1;96m',     '\033[46m',     '\033[0;106m'
whi,     bwhi,     uwhi,     iwhi,     biwhi,     on_whi,     on_iwhi = '\033[0;37m',     '\033[1;37m',     '\033[4;37m',     '\033[0;97m',     '\033[1;97m',     '\033[47m',     '\033[0;107m'


def text(s='', cc=bigre, es=''):
    return cc+s+nocolor+es

def cprint(s='', cc=bigre, es=''):
    print(cc+s+nocolor+es)

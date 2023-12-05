from limits import get_limits

OW = {
"SLC":27691,
"SLO":24207,
"SLK":28380,
"SLD":23633
}


departure = input('Airport: ').upper()
temp = int(input('Temperature: '))
aircraft = input('Aircraft: ').upper()
fuel = int(input('Fuel: '))
adults = 0 #start with zero adults
children = int(input('Children: ')) #start with children only
bgg = input('Fixed or Standard bgg: ').lower()


if bgg in ['fixed','f', 'fix']:
    bgg_wt = int(input('Bgg: '))
elif bgg in ['standard', 's', 'std']:
    bgg_wt = children * 31


print('\n')
print(f'MAX PAYLOAD WITH {children}CH')
RTOW = get_limits(aircraft, departure, temp)

empty_wt = OW[aircraft]
TOW = empty_wt + fuel + children*75 + bgg_wt - 50


if bgg in ['fixed','f', 'fix']:
    while TOW <= RTOW:
        adults += 1
        TOW += 185
    else:
        adults -= 1
        TOW -= 185
elif bgg in ['standard', 's', 'std']:
    while TOW <= RTOW:
        adults += 1
        TOW += 216
        bgg_wt += 31
    else:
        adults -= 1
        TOW -= 216
        bgg_wt -= 31


TOB = adults + children
underload = RTOW - TOW


if aircraft == 'SLK':
    if TOB > 52:
        adults = 52 - children
        TOB = 52
        if bgg in ['s','standard', 'std']:
            bgg_wt = 52 * 31
            TOW = empty_wt + fuel + adults*185 + children*75 + bgg_wt - 50
            underload = RTOW - TOW
        else:
            TOW = empty_wt + fuel + adults*185 + children*75 + bgg_wt - 50
            underload = RTOW - TOW

elif aircraft == "SLC":
    if TOB > 50:
        adults = 50 - children
        TOB = 50
        if bgg in ['s','standard', 'std']:
            bgg_wt = 50 * 31
            TOW = empty_wt + fuel + adults*185 + children*75 + bgg_wt - 50
            underload = RTOW - TOW
        else:
            TOW = empty_wt + fuel + adults*185 + children*75 + bgg_wt - 50
            underload = RTOW - TOW

else:
    if TOB > 37:
        adults = 37 - children
        TOB = 37
        if bgg in ['s','standard', 'std']:
            bgg_wt = 37 * 31
            TOW = empty_wt + fuel + adults*185 + children*75 + bgg_wt - 50
            underload = RTOW - TOW
        else:
            TOW = empty_wt + fuel + adults*185 + children*75 + bgg_wt - 50
            underload = RTOW - TOW


print(f'Pax: \t\t {adults + children}')
print(f'Bgg: \t\t {bgg_wt}')
print(f'TOW: \t\t {TOW}')
print(f'Underload: \t {underload}')

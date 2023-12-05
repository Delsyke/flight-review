from limits import get_limits

OW = {
"SLC":27691,
"SLO":24207,
"SLK":28380,
"SLD":23633
}

departure = input('Airport: ').upper()
# aircraft = input('Aircraft: ').upper()
temp = int(input('Temperature: '))
fuel = int(input('Fuel: '))
children = int(input('Children: ')) #start with children only
bgg = input('Fixed or Standard bgg: ').lower()

if bgg in ['fixed','f', 'fix']:
    bgg_wt = int(input('Bgg: '))
elif bgg in ['standard', 's', 'std']:
    bgg_wt = children * 31


print('\n')
print(f'MAX PAYLOADS WITH {children}CH: ')
def max_payload(aircraft, bgg_wt=bgg_wt):
    adults = 0 #start with zero adults
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

    return [adults, bgg_wt, TOW, underload]

# print('\n')
for aircraft in ['SLD', 'SLO', 'SLC', 'SLK']:
    print(f'\t-{aircraft}-')
    max_load = max_payload(aircraft)
    print(f'Pax: \t\t {max_load[0]+children}')
    print(f'Bgg: \t\t {max_load[1]}')
    print(f'TOW: \t\t {max_load[2]}')
    print(f'Underload: \t {max_load[3]}')
    print('\n')

import sys

def calc_geometric_betsize(args):

    if len(args) < 2:
        print('You must input pot-size and effective-stack-size!')
        sys.exit(1)

    if len(args) == 2:
        bet = 0
    else:
        bet = float(args[2])

    pot = args[0] + 2 * bet
    stack = args[1]
    spr = stack / pot
    target = 1 + 2 * spr

    two = (target ** (1/2) - 1 )/ 2
    three = (target ** (1/3) - 1 )/ 2
    four = (target ** (1/4) - 1 )/ 2

    print('stack: ',stack)
    print('pot: ', pot)
    print('spr: {:.2f}'.format(spr))

    print('Bet Two-Times to all-in: {:.1f} % of pot'.format(100*two))
    print('Bet Three-Times to all-in: {:.1f} % of pot'.format(100*three))
    print('Bet Four-TImes to all-in: {:.1f} % of pot'.format(100*four))


if __name__ == '__main__':
    calc_geometric_betsize(list(map(float, sys.stdin.readline().split()))) # pot, stack, bet
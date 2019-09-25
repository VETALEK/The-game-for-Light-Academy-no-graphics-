from random     import randint  as rnd
from datetime   import datetime as dtm
from sys        import platform
from os         import system   as command
from time       import sleep    as delay

class Character():

    def __init__(self, name, hp):
        self.name           = name.upper()
        self.max_hp         = hp
        self.hp             = hp
        #the state in the battle ( like 'DEAD' or 'ATTACKING' )
        self.state          = 'U shuldn\'t see that'
        #the logs about what happened during the battle
        self.history        = [ '_' * ( self.lineLength - 1 ) + ' ' for i in range(15) ]

    def EasyAttack(self, victim):
        dmg         = rnd(15, 25)
        victim.hp   -= dmg
        #adding the logs about the action
        self.AddToHistory( '[{}] Dealt {} damage with \'Easy attack\';'.format(self.currentTime, dmg) )
        victim.AddToHistory( '[{}] Got {} damage;'.format(self.currentTime, dmg) )

    def SrongAttack(self, victim):
        dmg         = rnd(10, 35)
        victim.hp   -= dmg
        #adding the logs about the action
        self.AddToHistory( '[{}] Dealt {} dmg with \'Strong attack\';'.format(self.currentTime, dmg) )
        victim.AddToHistory( '[{}] Got {} dmg;'.format(self.currentTime, dmg) )

    def Heal(self, victim):
        dmg     = rnd(15, 25)
        self.hp += dmg
        #adding the logs about the action
        self.AddToHistory( '[{}] Restored {} hp with \'Heal\';'.format(self.currentTime, dmg) )
        victim.AddToHistory( '[{}] Wasn\'t attacked;'.format(self.currentTime) )

    #for adding a new action log to the history
    def AddToHistory(self, msg):
        for i in range( len(self.history) - 1 ):
            self.history[i] = self.history[i+1] + ' ' * ( self.lineLength - len( self.history[i+1] ) )
        self.history[-1] = msg + ' ' * ( self.lineLength - len(msg) )

    @property
    def currentTime(self):
        return str( dtm.now().time() )[:8]

    @property
    #the length of the longest message in history
    #necessary for cute look
    def lineLength(self):
        return 47

    @property
    #what will be written on the top
    def statusBar(self):
        bar = '[{}][{}/{}][{}]'.format(self.name, self.hp, self.max_hp, self.state)
        bar += ':' * ( self.lineLength - len(bar) )
        return bar


class Bot(Character):

    def __init__(self, name, hp):
        super().__init__(name, hp)

    def GiveTurnTo(self, target, delay_time):
        self.state      = 'DEFENDING'
        #to prevent '-10/100hp'
        if target.hp <= 0:
            target.hp       = 0
            target.state    = 'DEFEATED'  
            self.state      = 'WON'  
        else:
            target.state    = 'ATTACKING'
        #to prevent '101/100hp'
        if self. hp > self.max_hp:
            self.hp = self.max_hp

        delay(delay_time)
        if platform == 'linux':
            command('clear')
        else:
            command('cls')
        #show the info about fighters
        print( target.statusBar + self.statusBar + '\n' * 2 )
        #show battle logs
        for i in range( len(self.history) ):
            print( target.history[i] + self.history[i] )

    def DoRandAction(self, victim):
        msg = 'WAIT A BIT'
        print( '\n\n\n{0}{1}{0}'.format( ':' * ( ( 2 * self.lineLength - len(msg) ) // 2 ), msg ) )
        #no 'HEAL"
        #bcoz it is no sense to heal whrn u r with full hp
        actions = [ self.EasyAttack, self.SrongAttack ]
        if self.hp < self.max_hp:
        #allow healing if hp is not full
            actions.append( self.Heal )
        #increase the chance oh 'HEAL'
        if self.hp <= 35:
            actions.append( self.Heal )
        actions[ rnd( 0, len(actions) - 1 ) ](victim)


class Player(Character):

    def __init__(self, name, hp):
        super().__init__(name, hp)

    def GiveTurnTo(self, target, delay_time):
        self.state      = 'DEFENDING'
        if target.hp <= 0:
            target.hp       = 0
            target.state    = 'DEFEATED'
            self.state      = 'WON'
        else:
            target.state    = 'ATTACKING'
        if self. hp > self.max_hp:
            self.hp = self.max_hp

        delay(delay_time)
        if platform == 'linux':
            command('clear')
        else:
            command('cls')
        #show the info about fighters
        print( self.statusBar + target.statusBar + '\n' * 2 )
        #show battle logs
        for i in range( len(self.history) ):
            print( self.history[i] + target.history[i] )

    def DoRandAction(self, victim):
        msg = 'PRESS [ENTER] TO MAKE A RANDOM ACTION'
        input( '\n\n\n{0}{1}{0}'.format( ':' * ( ( 2 * self.lineLength - len(msg) ) // 2 ), msg ) )
        #no 'HEAL"
        #bcoz it is no sense to heal whrn u r with full hp
        actions = [ self.EasyAttack, self.SrongAttack ]
        #allow healing if hp is not full
        if self.hp < self.max_hp:
            actions.append( self.Heal )
        actions[ rnd( 0, len(actions) - 1 ) ](victim)


class BattleManager():

    def __init__(self, player, enemy):
        self.players = [ player, enemy ]

    #render the battle logs
    def Manage(self, delay_time):
        #randomize the turns queue
        turn = rnd( 0, 1 )
        self.players[ turn % 2 - 1 ].GiveTurnTo( self.players[ (turn) % 2 ], delay_time )
        while self.players[0].hp > 0 and self.players[1].hp > 0:
            self.players[ turn % 2 ].DoRandAction( self.players[ turn % 2 - 1 ] )
            self.players[ turn % 2 ].GiveTurnTo( self.players[ turn % 2 - 1 ], delay_time )
            turn += 1
        #show an appropriate message in the end
        if self.players[0].hp <= 0 and not self.players[1].hp <= 0:
            self.ShowDefeatMsg()
        elif self.players[1].hp <= 0 and not self.players[0].hp <= 0:
            self.ShowWinMsg()
        else:
            self.ShowDrawMsg()

    def ShowWinMsg(self):
        lines = [
                'X         X    XXXXXX    X    X     XX',
                'X    X    X   X      X   X   X X   XXX',
                'X    X    X   X      X   X  X  X    X ',
                ' X  X X  X    X      X   X X   X      ',
                '  XX   XX      XXXXXX     X    X   XX '
                ]
        print( '\n' * 3 )
        for line in lines:
            print( '{0}{1}{0}'.format( ' ' * ( self.players[0].lineLength - ( len(line) // 2 ) ), line ) )

    def ShowDefeatMsg(self):
        lines = [
                'X          XXXXXX    XXXXXXX   XXXXXXX    XX',
                'X         X      X   X         X  X  X   XXX',
                'X         X      X   XXXXXXX      X       X ',
                'X         X      X         X      X         ',
                'XXXXXXX    XXXXXX    XXXXXXX     XXX     XX '
                ]
        print( '\n' * 3 )
        for line in lines:
            print( '{0}{1}{0}'.format( ' ' * ( self.players[0].lineLength - ( len(line) // 2 ) ), line ) )

    def ShowDrawMsg(self):
        lines = [
                'XXXXXX     XXXXXX      XXX     X         X    XX',
                'X     X    X     X    X   X    X    X    X   XXX',
                'X      X   XXXXXX    X     X   X    X    X    X ',
                'X      X   X    X    X XXX X    X  X X  X       ',
                'XXXXXX     X     X   X     X     XX   XX     XX '
                ]
        print( '\n' * 3 )
        for line in lines:
            print( '{0}{1}{0}'.format( ' ' * ( self.players[0].lineLength - ( len(line) // 2 ) ), line ) )


computer, player = Bot( 'Computer', 100 ), Player( 'Player', 100 )
mngr = BattleManager( player, computer )
mngr.Manage(1)
#to prevent closing the window
input()

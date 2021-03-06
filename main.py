import world
import elements #eventually, this won't be called
help_string='''To make the game advance a tick, press enter with the text box empty
To quit the game, enter 'q'
To see this again, enter 'help\''''
class game(object):
    def __init__(self, setup=0):
        self.w=world.world()
        if setup==0: 
            self.w.ground()
        elif setup==1:
            self.setup_ball_wall_coll()
        else:
            try:
                exec "self.setup_"+str(setup)+"()"
            except NameError:
                print "Non-existant setup"
                print "Defaulting to basic setup"
                self.w.ground()
    def run(self):
        cont=True
        while(cont):
            print self.w
            ans=raw_input("")
            if ans=="q":
                break
            if ans=='d':
                self.w.diagnose()
            self.w.tick()
    def setup_ball_wall_coll(self):
        a=elements.boulder(0,0,25,0,0)
        b=elements.rock(2,0)
        self.w.ground()
        self.w.add_struc(a)
        self.w.add_struc(b)
        print self.w
    def setup_2(self):
        wall=elements.rock(5,5)
        left=elements.boulder(0,5,25,0,0)
        top=elements.boulder(5,0,0,20,0)
        right=elements.boulder(10,5,-13,0,0)
        bottom=elements.boulder(5,10,0,-7,0)
        self.w.ground()
        self.w.add_struc(wall)
        self.w.add_struc(left)
        self.w.add_struc(top)
        self.w.add_struc(right)
        self.w.add_struc(bottom)
        print self.w
        #if raw_input("Good? ").strip().lower()=='y':
        #self.run()
        
    def setup_3(self):
        b1=elements.boulder(0,0,0,0,0)
        b2=elements.boulder(2,0,-5,0,0)
        b3=elements.boulder(0,5,2,0,0)
        b4=elements.boulder(9,5,-2,0,0)
        b5=elements.boulder(0,3,0,-2,0)
        self.w.ground()
        self.w.add_struc(b1)
        self.w.add_struc(b2)
        self.w.add_struc(b3)
        self.w.add_struc(b4)
        self.w.add_struc(b5)
        
    def tick(self, command):
        '''Reads the command and acts on it
        Outputs:
            1:Tick was run, print the world
            0:Game should now quit
            Something else:Print that
        Output2:
            String to print if a string wasn't passed as output1
        '''
        text=self.w.diagnose()
        if command=='':
            self.w.tick()
            return 1,text
        elif command=='q':
            return 0,text
        elif command=='help':
            return help_string, ''
        elif command.startswith('spawn'):
            return self.add(command), text
        elif command=='d':
            return self.w.diagnose(),''#now automatically called
        return 1,''
    def __repr__(self):
        return str(self.w)
    def draw_data(self):
        return self.w.fancy_print()
    def add(self, command):
        if not command.startswith("spawn"):
            print "Error: command of '%s' was identified as a spawn command"%command
            return False
        return self.w.spawn(command)
import interface
class master(object):
    def __init__(self):
        ans=raw_input("Use new input? y/N ").strip().lower()
        if ans=='y':
            self.mode='setup'
            self.inter=interface.interface(self, 10,10)
            self.inter.startup()#this call doesn't return until the window is closed, nothing will be run after it
            #print "done!"
            #self.inter.set_text('Enter the setup number')
            #print "New input is not yet coded"
            #self.interface_setup()
            #return
        else:
            ans=raw_input("Enter setup number: ").strip()
            if ans.isdigit()==False:
                ans=0
            else:
                ans=int(ans)
            self.game=game(ans)
            self.mainloop()
    def mainloop(self):
        while True:
            ans=raw_input(">")
            a,blah=self.game.tick(ans)
            if a==0:
                return
            elif a==1:
                print self.game
            elif type(a)==str:
                print a
    def recieve(self, value):
        if self.mode=='setup':
            self.game=game(int(value))
            self.mode='play'
            tile,flrs,stus=self.game.draw_data()
            self.inter.draw(tile,flrs,stus)
        elif self.mode=='play':
            a,text=self.game.tick(value)
            if text!='':        
                self.inter.set_text(text)
            if a==0:
                self.inter.end()
            elif a==1:
                #self.inter.set_text(str(self.game)) #eventually, will draw it
                tile,flrs,stus=self.game.draw_data()
                self.inter.draw(tile,flrs,stus)
            elif type(a)==str:
                self.inter.set_text(a)
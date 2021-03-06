import math
import re
import config_manager as cm
tile_size=cm.config['tile_size']#100
class id_manager(object):
    curr_id=0
    def next_id(self):
        val=self.curr_id
        self.curr_id+=1
        return val
ids=id_manager()
def type_from_string(var, string):
    '''Goes through the logic of string says 'int', so make var int'''
    try:
        if string=='int':
            return int(var)
        elif string=='str':
            return str(var)
        elif string=='float':
            return float(var)
    except ValueError:
        print "invalid value for type"
        if string=='int' or string=='float':
            return 0
        if string=='str':
            return ''
class element(object):
    '''Basic map element class'''
    args=['x','y','sprite','color']
    def __init__(self, x=0, y=0, sprite=' ', color='white'):
        self.x=x*tile_size
        self.y=y*tile_size
        self.sprite=sprite
        self.color=color
    @staticmethod
    def split_args(comm):
        '''splits up large 'name=val' into a dictionary of name:val'''
        vals={}
        names=re.findall('(\S+)\s?=',comm)
        values=re.findall("=\s?([\d\.\-]+|['\"]\S+['\"])",comm)
        if len(values)!=len(names):
            #print len(values)
            #print len(names)
            return False
        for i in range(len(names)):
            if values[i].startswith("'"):
                vals[names[i]]=values[i][1:-1]
            else:
                try:
                    vals[names[i]]=float(values[i])
                except ValueError:
                    vals[names[i]]=values[i]
        return vals
    @classmethod
    def from_comm(cls, comm):
        vals=cls.split_args(comm)
        if vals==False:
            #print "umm..."
            return False
        for val in vals.keys():
            if val not in cls.args:
                vals.pop(val)
        return cls(**vals)
    def is_floor(self):
        return False
class floor(element):
    '''So, I realized that the base case is there being ground, so now this is just background, holes & stuff will be structures'''
    args=['x','y','sizex','sizey','sprite','color']
    def __init__(self, x=0, y=0, sizex=1, sizey=1, sprite=' ', color='white'):
        self.x=x*tile_size
        self.y=y*tile_size
        self.sx=sizex*tile_size
        self.sy=sizey*tile_size
        self.sprite=sprite
        self.color=color
    def is_floor(self):
        return True
class ground(floor):
    args=['x','y', 'sizex','sizey']
    def __init__(self, x=0, y=0, sizex=1,sizey=1):
        floor.__init__(self, x, y,sizex,sizey, '.', 'white')
class structure(element):
    type_name="Generic structure"
    args=['x','y','sprite','color','box_length','collision_class','speedx','speedy','friction']
    def __init__(self, x=0, y=0,speedx=0,speedy=0,friction=0, sprite=' ',color='white', box_length=1, collision_class='wall'):
        element.__init__(self,x,y,sprite,color)
        #self.x=x*tile_size
        #self.y=y*tile_size
        self.dx=speedx
        self.dy=speedy
        self.k=friction
        #self.sprite=sprite
        #self.owner=null_world() #ok, that just sounds cool to type
        self.sId=ids.next_id()
        self.size=box_length*tile_size
        self.ded=False
        self.coll=collision_class
        #self.color=color
        #need to add in dx and dy eventually
        self.last_tick={'x':self.x, 'y':self.y, 'dx':self.dx, 'dy':self.dy}
    def tick(self):
        self.last_tick={'x':self.x, 'y':self.y, 'dx':self.dx, 'dy':self.dy}#for a bit this was at the top...
        if (abs(self.dx)>tile_size or abs(self.dy)>tile_size):
            print "Warning, an object is moving fast enough to suffer relativistic effects."
        self.x+=self.dx
        self.y+=self.dy
        if (self.dx==0 and self.dy==0):
            return
        thet=math.atan2(self.dy, self.dx)
        d=math.sqrt(self.dx**2+self.dy**2)
        d-=(1.0*self.k)/tile_size #did I really forget to do this?
        if d<0:  #I feel like I may want to do some editing to this to make the friction/speed scale with tile_size
            d=0
        self.dx=round((d*math.cos(thet)),10)
        self.dy=round((d*math.sin(thet)),10)#the round fixes a few floating-point errors
    def assign_world(self, world):
        self.world=world
    def diagnose(self):
        val= self.type_name+" with sId "+str(self.sId)
        varbs=['x','y','dx','dy','k','sprite','sId','size','ded','coll_class']
        vals=[self.x,self.y,self.dx,self.dy,self.k,self.sprite,self.sId,self.size,self.ded,self.coll]
        for i in range(len(varbs)):
            val+= "\n\t%s: %s"%(str(varbs[i]),str(vals[i]))
        return val
    def is_floor(self):
        return False
class wall(structure):
    type_name='Wall'
    args=['x','y','sprite','color','box_length','collision_class']
    def __init__(self, x=0,y=0,sprite='W',color='grey',box_length=1,collision_class='wall'):
        structure.__init__(self,x,y,0,0,1000,sprite,color,box_length,collision_class)
class rock(structure):
    type_name="Rock"
    def __init__(self, x=0,y=0,speedx=0,speedy=0,friction=5, sprite='*',color='black', box_length=1, collision_class='wall'):
        structure.__init__(self,x,y,speedx,speedy,friction,sprite,color,box_length, collision_class)
        #self.dx,self.dy=0,0
    def diagnose(self):
        val=structure.diagnose(self)
        '''varbs=['dx','dy']
        vals=[self.dx,self.dy]
        for i in range(len(varbs)):
            val+= "\n\t%s: %s"%(str(varbs[i]),str(vals[i]))'''
        return val
class boulder(structure):
    type_name="Boulder"
    args=['x','y','speedx','speedy','friction','sprite','color','box_length','collision_class']
    def __init__(self, x=0, y=0, speedx=0, speedy=0, friction=1, sprite='o',color='brown', box_length=1, collision_class='ball'):
        structure.__init__(self, x, y, speedx, speedy, friction, sprite,color,box_length,collision_class)
    def tick(self): #needed to think back to physics to write this function
        self.last_tick={'x':self.x, 'y':self.y, 'dx':self.dx, 'dy':self.dy}#for a bit this was at the top...
        if (abs(self.dx)>tile_size or abs(self.dy)>tile_size):
            print "Warning, an object is moving fast enough to suffer relativistic effects."
        self.x+=self.dx
        self.y+=self.dy
        if (self.dx==0 and self.dy==0):
            return
        thet=math.atan2(self.dy, self.dx)
        d=math.sqrt(self.dx**2+self.dy**2)
        d-=(1.0*self.k)/tile_size #did I really forget to do this?
        if d<0:  #I feel like I may want to do some editing to this to make the friction/speed scale with tile_size
            d=0
        self.dx=round((d*math.cos(thet)),10)
        self.dy=round((d*math.sin(thet)),10)#the round fixes a few floating-point errors
    def test_ticks(self):
        while True:
            self.tick()
            print "x:%d, y:%d, pos:(%d, %d), dx:%f, dy:%f"%(self.x,self.y,self.x/tile_size,self.dy/tile_size,self.dx,self.dy)
            if raw_input(""):
                break
    def test_run(self):
        print "Start: x:%3d, y:%d, pos:(%d, %d), dx:%f, dy:%f"%(self.x,self.y,self.x/tile_size,self.dy/tile_size,self.dx,self.dy)
        a=0
        while self.dx!=0 or self.dy!=0:
            self.tick()
            a+=1
            if a%10==0:
                print "After %3d ticks: x:%d, y:%d, pos:(%d, %d), dx:%f, dy:%f"%(a,self.x,self.y,self.x/tile_size,self.dy/tile_size,self.dx,self.dy)
        print "Finished after %3d ticks: x:%d, y:%d, pos:(%d, %d), dx:%f, dy:%f"%(a,self.x,self.y,self.x/tile_size,self.dy/tile_size,self.dx,self.dy)
    def diagnose(self):
        val=structure.diagnose(self)
        '''varbs=['dx','dy','k']
        vals=[self.dx,self.dy,self.k]
        for i in range(len(varbs)):
            val+= "\n\t%s: %s"%(str(varbs[i]),str(vals[i]))'''
        return val

/**
 * A test object
 *
 * @Eli
 * @0.1
 */
package objects;
public class rock extends obj
{
    private String name;
    private String desc;
    public rock(int x, int y){
        this(x, y, "Rock", "It is a rock");
    }
    public rock(int x, int y, String name, String desc){
        super(x, y);
        this.name=name;
        this.desc=desc;
    }
    public String desc(){
        return desc;
    }
    public String name(){
        return name;
    }
    public String draw(){
        return "*";
    }
    public void tick(){
        System.out.println("Test");
    }
    public String info(){
        String info=name+"\tID: "+get_id();
        info+="\n\t"+desc;
        info+="\n\tx: "+get_x()+"\n\ty: "+get_y();
        return info;
    }
}
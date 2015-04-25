/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package client.gui;

import client.core.Session;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import javax.swing.ImageIcon;

/**
 *
 * @author edmundophie
 */
public class GrandQuest {
    public final static String STATUS_OK = "ok";
    public final static String STATUS_FAIL = "fail";
    public final static String STATUS_ERROR = "error";
    public static Session SESSION;
    public static MainFrame FRAME;
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        FRAME = new MainFrame();
        
        FRAME.setTitle("LOGIN");
            FRAME.setVisible(true);
    }
    
    public static ImageIcon philStoneImg;
    public static ImageIcon elixirImg;
    public static ImageIcon crystalImg;
    public static ImageIcon potionImg;
    public static ImageIcon incenseImg;
    public static ImageIcon gemsImg;
    public static ImageIcon honeyImg;
    public static ImageIcon herbsImg;
    public static ImageIcon clayImg;
    public static ImageIcon mineralImg;
            
    public final static String PHILSTONE_FILE = "resources/images/phil_stone.png";
    public final static String ELIXIR_FILE = "resources/images/elixir.png";
    public final static String CRYSTAL_FILE = "resources/images/crystal.png";
    public final static String POTION_FILE = "resources/images/potion.png";
    public final static String INCENSE_FILE = "resources/images/incense.png";
    public final static String GEMS_FILE = "resources/images/gems.png";
    public final static String HONEY_FILE = "resources/images/honey.png";
    public final static String HERBS_FILE = "resources/images/herbs.png";
    public final static String CLAY_FILE = "resources/images/clay.png";
    public final static String MINERAL_FILE = "resources/images/mineral.png";
    
    public final static String gridFile = "resources/images/grid.jpg";
    public final static String characterFile = "resources/images/character.png";
}

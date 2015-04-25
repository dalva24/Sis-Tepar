/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package client.core;

import javafx.util.Pair;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

/**
 *
 * @author edmundophie
 */
public class Session {
    private boolean loggedIn;
    private final String username;
    private final String token;
    public long time;
    public Pair position;
    public static int[] itemCount = new int[10];
    
    public Session(String username, String token, int x, int y, long time) {
        this.username = username;
        this.token = token;
        this.position = new Pair(x, y);
        this.time = time;
    }
    public boolean isLoggedIn(){return loggedIn;}
    
    public void login(){loggedIn=true;}
    
    public void logout(){loggedIn=false;}
    
    public String getUsername() {return username;}
    
    public String getToken() {return token;}
    
    public long getTime() {return time;}
    
    public Pair getPosition() {return position;}
    
    public int getPosX() {return (int) position.getKey();}
    
    public int getPosY() {return (int) position.getValue();}
    
    public void setTime(long time) {this.time=time;}
    
    public void setPosition(Pair position) {this.position=position;}
    
    public void refreshItemCount(){
        JSONObject request = new JSONObject();
        request.put("method", "inventory");
        request.put("token", token);
        Connection conn = new Connection();
        JSONObject response = conn.sendToServer(request);
        JSONArray arr = (JSONArray) response.get("inventory");
        for(int i=0;i<arr.size();++i)
            itemCount[i]=Integer.parseInt(arr.get(i).toString());
    };
}

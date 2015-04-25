/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package client.core;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import static java.lang.System.in;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

/**
 *
 * @author edmundophie
 */
public class Connection {
    public static String SERVER_ADDRESS;
    public static int PORT;
    private Socket client;
    
    public Connection() {
        try {
            client = new Socket(SERVER_ADDRESS, PORT);
        } catch (IOException ex) {
            System.err.println(ex);
        }
    }
    
    public Connection(String server, int port) {
        SERVER_ADDRESS = server;
        PORT = port;
        try {
            client = new Socket(SERVER_ADDRESS, PORT);
        }   catch (IOException ex) {
            System.err.println(ex);
        }
    }
    
    public JSONObject sendToServer(JSONObject data) {
        JSONObject responseObj = null;
        try {
            // Send data to server
            PrintWriter out = new PrintWriter(client.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
            BufferedReader stdIn =new BufferedReader(new InputStreamReader(System.in));
            out.println(data.toJSONString());
            
            // Get response from server
            String response = in.readLine();
            System.out.println(response);
            JSONParser parser = new JSONParser();
            responseObj = (JSONObject) parser.parse(response);
            client.close();
        } catch (IOException | ParseException ex) {
            System.err.println(ex);
        }
        
        return responseObj;
    }
}

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package client.driver;

import client.core.Connection;
import client.gui.GrandQuest;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

/**
 *
 * @author edmundophie
 */
public class Tester {
    public static void main(String[] args) {
        String hostName = "167.205.32.46";
        int portNumber = 8025;
        
        JSONObject data = new JSONObject();
        data.put("method", "signup");
        data.put("username", "jokowi");
        data.put("password", "widodo");
        try {
            Socket client = new Socket(hostName, portNumber);
            PrintWriter out = new PrintWriter(client.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
            BufferedReader stdIn =new BufferedReader(new InputStreamReader(System.in));
            out.println(data.toJSONString());
            String response = in.readLine();
            System.out.println(response);
        } catch (IOException ex) {
            System.err.println(ex);
        }
    }
}

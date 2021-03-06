/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package client.gui;

import client.core.Connection;
import client.core.Session;
import java.awt.CardLayout;
import javax.swing.JOptionPane;
import org.json.simple.JSONObject;

/**
 *
 * @author edmundophie
 */
public class LoginPane extends javax.swing.JPanel {
    private javax.swing.JPanel cards;
    private final static String LOGIN = "login";
    private final static String REGISTER = "signup";
    private String MODE;
    /**
     * Creates new form LoginPane
     */
    public LoginPane(javax.swing.JPanel cards) {
        this.cards = cards;
        initComponents();
        MODE = LOGIN;
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jLabel1 = new javax.swing.JLabel();
        jLabel2 = new javax.swing.JLabel();
        jTextField1 = new javax.swing.JTextField();
        jTextField2 = new javax.swing.JTextField();
        jLabel3 = new javax.swing.JLabel();
        jButton1 = new javax.swing.JButton();
        jLabel4 = new javax.swing.JLabel();
        jTextField3 = new javax.swing.JTextField();
        jLabel5 = new javax.swing.JLabel();
        jTextField4 = new javax.swing.JTextField();
        deskripsiLbl = new javax.swing.JLabel();

        setLayout(new org.netbeans.lib.awtextra.AbsoluteLayout());

        jLabel1.setFont(new java.awt.Font("Lucida Grande", 1, 18)); // NOI18N
        jLabel1.setText("Password");
        add(jLabel1, new org.netbeans.lib.awtextra.AbsoluteConstraints(220, 240, -1, -1));

        jLabel2.setFont(new java.awt.Font("Chalkduster", 1, 28)); // NOI18N
        jLabel2.setText("LOGIN");
        add(jLabel2, new org.netbeans.lib.awtextra.AbsoluteConstraints(340, 110, -1, -1));
        add(jTextField1, new org.netbeans.lib.awtextra.AbsoluteConstraints(320, 230, 260, 40));
        add(jTextField2, new org.netbeans.lib.awtextra.AbsoluteConstraints(320, 180, 260, 40));

        jLabel3.setFont(new java.awt.Font("Lucida Grande", 1, 18)); // NOI18N
        jLabel3.setText("Username");
        add(jLabel3, new org.netbeans.lib.awtextra.AbsoluteConstraints(220, 190, -1, -1));

        jButton1.setFont(new java.awt.Font("Lucida Grande", 1, 14)); // NOI18N
        jButton1.setText("LOGIN");
        jButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton1ActionPerformed(evt);
            }
        });
        add(jButton1, new org.netbeans.lib.awtextra.AbsoluteConstraints(480, 350, 100, 40));

        jLabel4.setForeground(new java.awt.Color(51, 51, 255));
        jLabel4.setText("Register");
        jLabel4.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent evt) {
                jLabel4MouseClicked(evt);
            }
        });
        add(jLabel4, new org.netbeans.lib.awtextra.AbsoluteConstraints(420, 360, -1, -1));

        jTextField3.setText("8026");
        add(jTextField3, new org.netbeans.lib.awtextra.AbsoluteConstraints(580, 280, 70, 40));

        jLabel5.setFont(new java.awt.Font("Lucida Grande", 1, 18)); // NOI18N
        jLabel5.setText("Server");
        add(jLabel5, new org.netbeans.lib.awtextra.AbsoluteConstraints(220, 290, -1, -1));

        jTextField4.setText("167.205.32.46");
        add(jTextField4, new org.netbeans.lib.awtextra.AbsoluteConstraints(320, 280, 260, 40));
        add(deskripsiLbl, new org.netbeans.lib.awtextra.AbsoluteConstraints(220, 330, -1, -1));
    }// </editor-fold>//GEN-END:initComponents

    private void jLabel4MouseClicked(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_jLabel4MouseClicked
        toggleMode();
    }//GEN-LAST:event_jLabel4MouseClicked

    private void toggleMode() {
        if(jLabel4.getText().equals("Register")) {
            jLabel2.setText("REGISTER");
            jButton1.setText("REGISTER");
            jLabel4.setText("Login");
            MODE = REGISTER;
        } else {
            jLabel2.setText("LOGIN");
            jButton1.setText("LOGIN");
            jLabel4.setText("Register");
            MODE = LOGIN;
        }
    }
    
    private void jButton1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton1ActionPerformed
        // Get register data
        String username = jTextField2.getText();
        String password = jTextField1.getText();
        String serverAddr = jTextField4.getText();
        int port = Integer.parseInt(jTextField3.getText());
            
        JSONObject response = processAction(username, password, serverAddr, port);
        
        // Response handling
        if(response.get("status").equals(GrandQuest.STATUS_OK)) {
            if(MODE == LOGIN) {

                // Create new session
                GrandQuest.SESSION = new Session(username, response.get("token").toString(),
                                        ((Long)response.get("x")).intValue(), 
                                        ((Long)response.get("y")).intValue(), 
                                        (Long)response.get("time"));   
                GrandQuest.SESSION.login();
                GrandQuest.FRAME.getPane(MainFrame.MAP).reloadContent();        // Reload Map Content
                ((CardLayout) cards.getLayout()).show(cards, MainFrame.MAP);    // Show map
            } else if(MODE == REGISTER){
                JOptionPane.showMessageDialog(this, MODE.substring(0, 1).toUpperCase() + MODE.substring(1) + " berhasil! ", "SIGNUP SUCCESS", JOptionPane.INFORMATION_MESSAGE);
                toggleMode();
            }
        } else if(response.get("status").equals(GrandQuest.STATUS_FAIL)) { 
            JOptionPane.showMessageDialog(this, MODE.substring(0, 1).toUpperCase() + MODE.substring(1) + " GAGAL! " + response.get("description"), "FAIL", JOptionPane.ERROR_MESSAGE);
        } else { // STATUS_ERROR
            deskripsiLbl.setText(MODE.substring(0, 1).toUpperCase() + MODE.substring(1) + " ERROR!");
            JOptionPane.showMessageDialog(this, MODE.substring(0, 1).toUpperCase() + MODE.substring(1) + " ERROR! ", "ERROR", JOptionPane.ERROR_MESSAGE);
        } 
    }//GEN-LAST:event_jButton1ActionPerformed

    private JSONObject processAction(String username, String password, String server, int port) {
        // Create request data to json
        JSONObject requestObj =  new JSONObject();
        requestObj.put("method", MODE);
        requestObj.put("username", username);
        requestObj.put("password", password);
        
        // Make connection to server
        Connection conn = new Connection(server, port);
        
        return conn.sendToServer(requestObj); // Send request & get response from server
    }
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JLabel deskripsiLbl;
    private javax.swing.JButton jButton1;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JLabel jLabel5;
    private javax.swing.JTextField jTextField1;
    private javax.swing.JTextField jTextField2;
    private javax.swing.JTextField jTextField3;
    private javax.swing.JTextField jTextField4;
    // End of variables declaration//GEN-END:variables
}

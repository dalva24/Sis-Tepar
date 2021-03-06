/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package client.gui;

import client.core.Connection;
import java.awt.CardLayout;
import java.awt.Component;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

/**
 *
 * @author edmundophie
 */
public class TradingPane extends javax.swing.JPanel implements WindowPane {
    private javax.swing.JPanel cards;
    public static JSONArray SEARCH_RESULT;
    
    /**
     * Creates new form LoginPane
     */
    public TradingPane(javax.swing.JPanel cards) {
        this.cards = cards;
        initComponents();
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jScrollPane1 = new javax.swing.JScrollPane();
        jPanel1 = new javax.swing.JPanel();
        jLabel2 = new javax.swing.JLabel();
        jLabel3 = new javax.swing.JLabel();
        jLabel4 = new javax.swing.JLabel();
        jLabel5 = new javax.swing.JLabel();
        jLabel6 = new javax.swing.JLabel();
        jButton3 = new javax.swing.JButton();

        jPanel1.setLayout(new java.awt.GridLayout(0, 5));
        jScrollPane1.setViewportView(jPanel1);

        jLabel2.setFont(new java.awt.Font("Lucida Grande", 1, 14)); // NOI18N
        jLabel2.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel2.setText("Offered Item");

        jLabel3.setFont(new java.awt.Font("Lucida Grande", 1, 14)); // NOI18N
        jLabel3.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel3.setText("Number Offered");

        jLabel4.setFont(new java.awt.Font("Lucida Grande", 1, 14)); // NOI18N
        jLabel4.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel4.setText("Demanded Item");

        jLabel5.setFont(new java.awt.Font("Lucida Grande", 1, 14)); // NOI18N
        jLabel5.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel5.setText("Number Demanded");

        jLabel6.setFont(new java.awt.Font("Lucida Grande", 1, 14)); // NOI18N
        jLabel6.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel6.setText("Act");

        jButton3.setText("Back");
        jButton3.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton3ActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jScrollPane1)
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addGap(0, 30, Short.MAX_VALUE)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                                .addComponent(jLabel2)
                                .addGap(47, 47, 47)
                                .addComponent(jLabel3)
                                .addGap(43, 43, 43)
                                .addComponent(jLabel4)
                                .addGap(46, 46, 46)
                                .addComponent(jLabel5)
                                .addGap(68, 68, 68)
                                .addComponent(jLabel6)
                                .addGap(69, 69, 69))
                            .addComponent(jButton3, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.PREFERRED_SIZE, 110, javax.swing.GroupLayout.PREFERRED_SIZE))))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGap(9, 9, 9)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jLabel2)
                    .addComponent(jLabel3)
                    .addComponent(jLabel4)
                    .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                        .addComponent(jLabel5)
                        .addComponent(jLabel6)))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 457, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(37, 37, 37)
                .addComponent(jButton3, javax.swing.GroupLayout.PREFERRED_SIZE, 40, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(34, Short.MAX_VALUE))
        );
    }// </editor-fold>//GEN-END:initComponents

    private void jButton3ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton3ActionPerformed
        GrandQuest.FRAME.getPane(MainFrame.FIND).reloadContent();
        ((CardLayout) cards.getLayout()).show(cards, MainFrame.FIND);
    }//GEN-LAST:event_jButton3ActionPerformed


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton jButton3;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JLabel jLabel5;
    private javax.swing.JLabel jLabel6;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JScrollPane jScrollPane1;
    // End of variables declaration//GEN-END:variables

    @Override
    public void reloadContent() {
        jPanel1.removeAll();
        JSONArray offers = SEARCH_RESULT;
        for(int i=0;i<offers.size();++i) {
            // Add component
            JSONArray offer = (JSONArray) offers.get(i);
            if((boolean)offer.get(4)) { // Get offer availability
                JLabel offeredLbl = new JLabel();
                offeredLbl.setIcon(getItemIcon(((Long) offer.get(0)).intValue()));

                JLabel nOfferedLbl = new JLabel();
                nOfferedLbl.setText(offer.get(1).toString());

                JLabel demandedLbl = new JLabel();
                demandedLbl.setIcon(getItemIcon(((Long) offer.get(2)).intValue()));

                JLabel nDemandedLbl = new JLabel();
                nDemandedLbl.setText(offer.get(3).toString());

                JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));
                JButton buyButton = new JButton("Buy");
                buyButton.addActionListener(new ActionListener() {
                    @Override
                    public void actionPerformed(ActionEvent e) {
                        //Create request JSON
                        JSONObject request = new JSONObject();
                        request.put("method", "sendaccept");
                        request.put("token", GrandQuest.SESSION.getToken());
                        request.put("offer_token", offer.get(5));

                        // Send request and get response        
                        Connection conn = new Connection();
                        JSONObject response = conn.sendToServer(request);
                        System.out.println(response);
                        if(response.get("status").equals(GrandQuest.STATUS_OK)) {
                            JOptionPane.showMessageDialog((Component) GrandQuest.FRAME.getPane(MainFrame.TRADING), "Trade has been made\nItem has been added to your inventory", "TRADE SUCCESS", JOptionPane.INFORMATION_MESSAGE);
                        } else if(response.get("status").equals(GrandQuest.STATUS_FAIL)) {
                            JOptionPane.showMessageDialog((Component) GrandQuest.FRAME.getPane(MainFrame.TRADING), "Trade can't be made\n" + response.get("description"), "TRADE FAILED", JOptionPane.ERROR_MESSAGE);
                        } else { // STATUS_ERROR
                            JOptionPane.showMessageDialog((Component) GrandQuest.FRAME.getPane(MainFrame.TRADING), "Server return an error", "TRADE ERROR", JOptionPane.ERROR_MESSAGE);
                        }

                        // Refresh pane
                        GrandQuest.FRAME.getPane(MainFrame.TRADING).reloadContent();
                        ((CardLayout) cards.getLayout()).show(cards, MainFrame.TRADING);
                    }
                });
                buttonPanel.add(buyButton);
                jPanel1.add(offeredLbl);
                jPanel1.add(nOfferedLbl);
                jPanel1.add(demandedLbl);
                jPanel1.add(nDemandedLbl);
                jPanel1.add(buttonPanel);
            }
        }
    }
    
    private ImageIcon getItemIcon(int itemId) {
        switch(itemId) {
            case 0: return GrandQuest.honeyImg;
            case 1: return GrandQuest.herbsImg;
            case 2: return GrandQuest.clayImg;
            case 3: return GrandQuest.mineralImg;
            case 4: return GrandQuest.potionImg;
            case 5: return GrandQuest.incenseImg;
            case 6: return GrandQuest.gemsImg;
            case 7: return GrandQuest.elixirImg;
            case 8: return GrandQuest.crystalImg;
            case 9: return GrandQuest.philStoneImg;
            default: return null;
        }
    }
}

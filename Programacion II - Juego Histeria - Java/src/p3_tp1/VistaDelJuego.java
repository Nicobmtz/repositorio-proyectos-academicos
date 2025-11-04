package p3_tp1;


import java.awt.*;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.border.LineBorder;
import javax.swing.SwingConstants;
import javax.swing.JLabel;

import java.awt.event.*;

public class VistaDelJuego implements Observer {


	private JPanel mainPanel;
	private JPanel gridPanel;
	private JPanel[][] paneles;
	private int tamanioGrilla; 
	private Logica logicaJuego;
	private int contadorClicks = 0;
    private JLabel lblContador;
	private Runnable volverAlMenu; 

	/**
	 * Create the application.
	 */
	public VistaDelJuego(int tamanioGrilla, Runnable volverAlMenu){
		this.tamanioGrilla = tamanioGrilla;
		this.logicaJuego = new Logica (tamanioGrilla);
		this.volverAlMenu = volverAlMenu;
	    logicaJuego.agregarObserver(this);
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {

        mainPanel = new JPanel(new BorderLayout());
        lblContador = new JLabel("Clicks: 0");
        lblContador.setHorizontalAlignment(SwingConstants.RIGHT);
        JPanel norte = new JPanel(new BorderLayout());
        norte.add(lblContador, BorderLayout.EAST);
        mainPanel.add(norte, BorderLayout.NORTH);

        gridPanel = new JPanel();
        gridPanel.setBorder(new LineBorder(new Color(0, 0, 0)));
        mainPanel.add(gridPanel, BorderLayout.CENTER);

        createGrid(tamanioGrilla);
		
	}
	
	
	private void createGrid (int tamanio) {
		gridPanel.removeAll();
		gridPanel.setLayout(new GridLayout(tamanio, tamanio));
		paneles = new JPanel[tamanio][tamanio];
		
		for (int fila = 0; fila < tamanio; fila++) {
			for (int col = 0; col < tamanio; col++) {
				JPanel panel = new JPanel();
              panel.setBorder(new LineBorder(Color.BLACK, 1));
              panel.setOpaque(true);             
              paneles[fila][col] = panel;
              gridPanel.add(panel); 
              paneles[fila][col].setBackground(Color.GRAY);
				
			}
		}
		asignarActionListener(tamanio);
		gridPanel.revalidate();
		gridPanel.repaint();
	}
	
	private void asignarActionListener(int tamanio) {
		for (int fila = 0; fila < tamanio; fila++) {
			int f=fila;
			for (int col = 0; col < tamanio; col++) {
				int c= col;

			
				paneles[fila][col].addMouseListener(new MouseAdapter() {
	                @Override
	                public void mousePressed(MouseEvent e) {  
                       contadorClicks++;
                       lblContador.setText("Clicks: " + contadorClicks);
	                   logicaJuego.jugar(f, c);
	                   actualizar(logicaJuego);
	                }
	            });			
			}
		}
	}

//	@Override
	public void actualizar(Logica logicaJuego){
	 for (int fila = 0; fila < paneles[0].length; fila++) {		
			for (int col = 0; col < paneles[0].length ; col++) {
			 paneles[fila][col].setBackground(logicaJuego.darColor(fila, col));
			}
	 }
	 
	 if (logicaJuego.FinDeJuego()== true) {
         String mensaje = logicaJuego.obtenerMensajeVictoria();
         JOptionPane.showMessageDialog(     mainPanel, mensaje,"Fin de Juego", JOptionPane.INFORMATION_MESSAGE );
		 volverAlMenu.run();
	 }
	}
	
    public JPanel getPanel() {
        return this.mainPanel;
    }
}

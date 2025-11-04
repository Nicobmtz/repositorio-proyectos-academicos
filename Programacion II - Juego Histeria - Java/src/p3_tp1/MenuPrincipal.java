package p3_tp1;

import java.awt.BorderLayout;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import java.awt.Image;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.SwingConstants;

public class MenuPrincipal {
	private JFrame frame;
	private Image menuImagen;
	private Image selecDificultad;

    public MenuPrincipal() {
        frame = new JFrame("Locura Cromática");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(500, 500);
        frame.setLayout(new BorderLayout());
        frame.setLocationRelativeTo(null); 
        menuImagen = new ImageIcon(getClass().getResource("/Histeria (1).gif")).getImage();
        selecDificultad = new ImageIcon(getClass().getResource("/Dificultad (1).gif")).getImage();
        
        mostrarMenu(); 
        frame.setVisible(true);
    }

    private void mostrarMenu() {
    	JPanel fondo = agregarFondo(menuImagen);
        JPanel panel = new JPanel(new GridLayout(4, 1, 10, 10)); 
        panel.setOpaque(false);
        
        //El Titulo
        JLabel titleLabel = new JLabel("Locura Cromática", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 20));
        panel.add(titleLabel);

        //Boton dificultades (facil, medio, dificil)
        JButton jugarButton = new JButton("Jugar");
        jugarButton.addActionListener(e -> mostrarSeleccionDificultad());
        panel.add(jugarButton);

        //Boton de Reglas
        JButton reglasButton = new JButton("Reglas");
        reglasButton.addActionListener(e -> JOptionPane.showMessageDialog(frame, "Reglas del juego: \n"
+ "    + 1. Haz clic en los botones para cambiar su color \n"
+ "    + 2. Si un botón coincide con el color de un vecino, ambos se reinician.\n"
+ "    + 3. Ganas cuando todos los botones tienen color y ninguno es gris."));
        panel.add(reglasButton);

        //Boton equipo
        JButton devsButton = new JButton("Devs");
        devsButton.addActionListener(e -> JOptionPane.showMessageDialog(frame, "Este juego fue creado por: \n" +
        		"Barboza Lola, Grande Federico, Martinez Nicole y Sanchez Lucía."));
        panel.add(devsButton);
        
        fondo.add(panel);

        actualizarPantalla(fondo);
    }

    //Botones de la dificultad
    private void mostrarSeleccionDificultad() {
    	JPanel fondo = agregarFondo(selecDificultad);
    	
        JPanel panel = new JPanel(new GridLayout(5, 5, 2, 20));
        panel.setOpaque(false);

        JLabel titleLabel = new JLabel("Selecciona una dificultad", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 18));
        panel.add(titleLabel);

        JButton facilButton = new JButton("Nivel Fácil (3x3)");
        facilButton.addActionListener(e -> iniciarJuego(3));
        panel.add(facilButton);

        JButton medioButton = new JButton("Nivel Medio (5x5)");
        medioButton.addActionListener(e -> iniciarJuego(5));
        panel.add(medioButton);

        JButton dificilButton = new JButton("Nivel Difícil (8x8)");
        dificilButton.addActionListener(e -> iniciarJuego(8));
        panel.add(dificilButton);

        //Mini boton volver al menu 
        JButton volverButton = new JButton("Volver al Menú");
        volverButton.addActionListener(e -> mostrarMenu());
        panel.add(volverButton); 
        fondo.add(panel);
        
        actualizarPantalla(fondo);
    }
    
    private JPanel agregarFondo (Image im){
    	JPanel fondo = new JPanel() {
                private Image imagen = im;

                @Override
                protected void paintComponent(Graphics g) {
                    super.paintComponent(g);
                    if (imagen != null) {
                        g.drawImage(imagen, 0, 0, getWidth(), getHeight(), this);
                    }
                }
            };
            fondo.setLayout(new GridBagLayout());
    	return fondo;
    }

    private void iniciarJuego(int tamanio) {
        JPanel juegoPanel = new JPanel(new BorderLayout()); 
        VistaDelJuego vistaJuego = new VistaDelJuego(tamanio, () -> mostrarMenu());
        juegoPanel.add(vistaJuego.getPanel(), BorderLayout.CENTER);

        JButton volverButton = new JButton("Volver al Menú");
        volverButton.addActionListener(e -> mostrarMenu());
        juegoPanel.add(volverButton, BorderLayout.SOUTH);

        actualizarPantalla(juegoPanel);
    }

    private void actualizarPantalla(JPanel nuevoPanel) {
        frame.getContentPane().removeAll();
        frame.getContentPane().add(nuevoPanel, BorderLayout.CENTER);
        frame.revalidate();
        frame.repaint();
    }

    public static void main(String[] args) {
        new MenuPrincipal();
    }

}

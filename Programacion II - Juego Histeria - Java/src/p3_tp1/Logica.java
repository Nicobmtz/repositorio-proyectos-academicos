package p3_tp1;

import java.awt.Color;
import java.util.ArrayList;
import java.util.Random;

public class Logica { 
	
	private Color [][] matrizColores;
	private  Color[] coloresPosibles = {Color.GRAY, Color.RED, Color.BLUE,Color.YELLOW, Color.ORANGE, Color.GREEN, Color.MAGENTA};
	private ArrayList <Observer> observers;

    private int contadorClicks = 0;
    private int limiteExxcelente; 
    private int bienLimite;/
	
	public  Logica(int celdas) { 
		this.matrizColores = new Color [celdas][celdas];
		configurarLimites(celdas);
		for (int fila = 0; fila < this.matrizColores[0].length ; fila++) {
			for (int colum= 0; colum < this.matrizColores[0].length ; colum++) {		
			this.matrizColores[fila][colum]= coloresPosibles[0];
			}
		}
		this.observers = new ArrayList <>();
		
	}
	
	public void comparaVecinos (int fila, int columna, Color color) {
		int [] xfila = {0, 1, 0, -1};
		int [] ycolum = {-1, 0, 1, 0};

		for (int i=0; i < xfila.length; i++) {
			int columnaComparar = columna + ycolum[i];
			int filaComparar = fila + xfila[i];

			if (columnaComparar >=0 && columnaComparar < this.matrizColores[0].length && filaComparar >=0 && filaComparar < this.matrizColores[0].length ){
				if (color.equals(this.matrizColores[filaComparar][columnaComparar])) {
					volverDefault(fila,columna);
					volverDefaultVecinos(fila, columna);			
				}
			}
		}
	}	
	

	

	public  boolean FinDeJuego () {
		
		boolean ningunoDefault = true;
		for (int fila = 0; fila < this.matrizColores[0].length ; fila++) {
			for (int colum= 0; colum < this.matrizColores[0].length ; colum++) {
			 ningunoDefault &= noesDefault(this.matrizColores[fila][colum]);
			}
		}
		return ningunoDefault;
	}
	
	private boolean noesDefault (Color celda) {
		return (celda != Color.GRAY); 			
	}

	//Colores
    private  Color colorAleatorio() {
    	Random random = new Random();
        int randomNumero = (random.nextInt(6)+1); 
        return coloresPosibles[randomNumero];
    }

    public void jugar(int fila, int columna) {
        contadorClicks++;
    	this.matrizColores[fila][columna]= colorAleatorio();
    	comparaVecinos(fila, columna,this.matrizColores[fila][columna]);	
    }
    
    public void asignarDefault(int fila, int columna) {
    	this.matrizColores[fila][columna]= this.coloresPosibles[0];
    }
    
   public Color darColor(int fila, int columna) {
    	Color c= this.matrizColores[fila][columna];
    	return c;
    }
   
   private void volverDefault(int fila, int col) {
	    asignarDefault(fila, col);
	    notificarObserver();
   }
   
	private void volverDefaultVecinos(int fila, int columna) {
		int [] xfila = {0, 1, 0, -1};
		int [] ycolum = {-1, 0, 1, 0};
		for (int i=0; i < xfila.length; i++) {
			int columnaComparar = columna + ycolum[i];
			int filaComparar = fila + xfila[i];
			if (columnaComparar >=0 && columnaComparar < this.matrizColores[0].length && filaComparar >=0
					&& filaComparar < this.matrizColores[0].length ){
				volverDefault(filaComparar,columnaComparar);
			}
		}	
	}
    
   
   
   //Observers
   public void agregarObserver(Observer obs) {
	   this.observers.add(obs);
   }
   
   private void notificarObserver() {
	   for (Observer obs : observers) {
		   obs.actualizar(this);	
	}
   }
   
   private void configurarLimites(int celdas) {
       if (celdas == 3) {
    	   limiteExxcelente = 12;
           bienLimite = 20;
       } else if (celdas == 5) {
    	   limiteExxcelente = 30;
           bienLimite = 45;
       } else if (celdas == 8) {
    	   limiteExxcelente = 65;
           bienLimite = 90;
       }
   }
   
   public String obtenerMensajeVictoria() {
       String message;
       if (contadorClicks <= limiteExxcelente) {
           message = "¡Excelente! Superaste el desafío con una gran estrategia\nHiciste " + contadorClicks + " clics.";
       } else if (contadorClicks <= bienLimite) {
           message = "¡Felicidades! Ganaste\nHiciste " + contadorClicks + " clics.";
       } else {
           message = "¡Bien! Pudiste terminarlo\nHiciste " + contadorClicks + " clics.";
       }
       return message;
   }
}

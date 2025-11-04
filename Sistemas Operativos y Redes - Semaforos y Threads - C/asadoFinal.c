#include <stdio.h> 
#include <pthread.h>
#include <semaphore.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

//Las variables
int invitados; 
int mozos;
int Manucho = 1;
int sentados = 0; // Contador de personas sentadas, se sienta +1. sentados=invitados, sumar a Manucho 
int platos; // Contador de comida servida


//Semaforos

sem_t sem_servir; // Se puede servir la comida, cuando se sienta Manucho
sem_t sem_sentarse; // Protección para modificar sentarse ++ 
sem_t sem_comer;

//sem de preg y resp
sem_t sem_levantarse; //levantarse e irse
sem_t sem_respuesta; //respuesta 
sem_t sem_una_respuesta; // Semáforo para controlar quién responde



void *sentarse(void *arg) { 
    int id = *((int *)arg);//Numero del invitado

    sem_wait(&sem_sentarse); 

    sentados++; 
    printf("Invitado %d se sienta.\n", id);

    if (sentados == invitados) { 
        printf("Manucho se sienta.\n");
	sem_post(&sem_servir);
    }
    sem_post(&sem_sentarse);
    return NULL;
}


 void* servirComida (void* arg){
    long id = (long)arg;
    while (platos > 0){    
         sem_wait (&sem_servir);

         platos= platos -1;
         printf("El mozo %ld, sirvio un plato \n", id );
         printf("Faltan servir %d platos \n \n", platos);

	 sem_post(&sem_comer);    
        
        sem_post(&sem_servir);
        sleep(1);
    }

return NULL;
}

void enojarse() {
    printf("Manucho se enojo y se levanto.\n");
    sem_post(&sem_levantarse);
}

void lanzar_pregunta_mundialista() {
    printf("Maradona o messi?? \n");
}

void levantarse(int id) {
    sem_wait(&sem_levantarse);
    printf("El invitado %d se levanto y se fue. \n", id);
    sem_post(&sem_levantarse);
}

void lanzar_respuesta_mundialista(int id) {
    printf("El invitado %d le responde: PELE \n", id);
    enojarse();
}


void terminoComer(int id){
    if (id == invitados) {
        printf("Manucho TERMINO a comer.\n");
        printf("Manucho hizo una pregunta mundialista\n");
        lanzar_pregunta_mundialista();
        sem_post(&sem_respuesta); // Permite que el invitado elegido responda
    } 
    else {
        printf("El invitado %d termino de comer \n", id);

        // Solo uno podrá ejecutar esta parte
        if (sem_trywait(&sem_una_respuesta) == 0) {
            sem_wait(&sem_respuesta); // espera la pregunta de Manucho
            lanzar_respuesta_mundialista(id);
        }
        levantarse(id);
    }
}

void* comer( void* arg){
    sem_wait(&sem_comer);
    int id = *((int*)arg);
    int tiempoComiendo = rand() % 11 + 5;
    
    if (id == invitados) {
        printf("Manucho comienza a comer.\n");
        sleep(tiempoComiendo); 
        terminoComer(id);
    } else {
        printf("Invitado %d comienza a comer.\n", id);
        sleep(tiempoComiendo);
        terminoComer(id);
    }
    return NULL;
}







int main() {
    //Ingresa cantidad de Invitados
    printf("Ingrese la cantidad de invitados: ");
    scanf("%d", &invitados);

    platos= invitados +1;



// Bucle para asegurarse de que haya menos mozos que invitados
    do {
    printf("Ingrese la cantidad de mozos (debe ser menor que la cantidad de invitados): ");
    scanf("%d", &mozos);
    
    if (mozos >= invitados) {
        printf("  La cantidad de mozos debe ser menor que la de invitados.\n");
    }
    } while (mozos >= invitados);


    //Hilos
    pthread_t* hilos_mozos = malloc(sizeof(pthread_t) * mozos);
    pthread_t* hilos_invitados = malloc(sizeof(pthread_t) * invitados);
    pthread_t* hilos_comer = malloc(sizeof(pthread_t) * (invitados + 1));    
   
    //id son los numeros de Invitados/Manucho/Mozos
    int* id_sentarse = malloc(sizeof(int) * invitados);
    int ids_comer[invitados + 1];

    //Inicialización de semaforos
    sem_init(&sem_servir, 0, 0);
    sem_init(&sem_sentarse, 0, 1);
    sem_init(&sem_levantarse, 0, 0);
    sem_init(&sem_respuesta, 0, 0);
    sem_init(&sem_una_respuesta, 0, 1); // solo un invitado puede responder
    sem_init(&sem_comer, 0, 0);

    //PAra el numero random
    srand(time(NULL));


//Invitados y manucho Hilos sentarse
   for (int i = 0; i < invitados; i++) { 
         id_sentarse[i] = i;
         pthread_create(&hilos_invitados[i], NULL, sentarse, &id_sentarse[i]);
    }


//The food is in the table
    for (long i = 0; i < mozos; i++){ 
       pthread_create(&hilos_mozos[i], NULL, servirComida, (void*)i);
    }

//Para que coman
    for (int i = 0; i <= invitados; i++) {
        ids_comer[i] = i;
        pthread_create(&hilos_comer[i], NULL, comer, &ids_comer[i]);
    }


//joins 
    for (int i = 0; i < invitados; i++) {
    pthread_join(hilos_invitados[i], NULL);
    }


    for (int i = 0; i<mozos; i++){ 
        pthread_join(hilos_mozos[i], NULL);
    }


    for (int i = 0; i <= invitados; i++) {
        pthread_join(hilos_comer[i], NULL);
}

    


    //Destruir semaforo 
    sem_destroy(&sem_servir);
    sem_destroy(&sem_sentarse);
    sem_destroy(&sem_levantarse);
    sem_destroy(&sem_respuesta);
    sem_destroy(&sem_una_respuesta);


    // Liberar memoria
    free(hilos_mozos);
    free(hilos_invitados);
    free(hilos_comer);
    free(id_sentarse);



    return 0;
}

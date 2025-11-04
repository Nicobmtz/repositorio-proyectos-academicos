# Proyecto: El Gran Asado

Este proyecto simula un almuerzo entre compañeros, donde la figura principal es *Manucho*, quien invita a todos a comer y contrata mozos para servir la comida.

Cuando Manucho se sienta, los invitados comienzan a comer. Durante la comida, Manucho realiza una pregunta sobre el mundial, a la que solo un invitado debe responder.  
Una vez que Manucho termina de comer, los invitados que ya hayan finalizado pueden levantarse.

---

##  Objetivo del Proyecto

- Aplicar conceptos de sincronización y programación concurrente.
- Coordinar tareas utilizando semáforos.
- Implementar concurrencia mediante el uso de hilos (threads).

---

## Tecnologías y Herramientas

- **Lenguaje:** C  
- **Librerías:** `pthreads`, `semaphore`  
- **Sistema Operativo:** Linux

---

## Contenido del repositorio

- `asadoFial.c`: Código fuente del proyecto  
- `miniTP2 de threads y Semáforos.pdf`: Enunciado del trabajo  
- `Informe Trabajo Práctico 2.pdf`: Informe técnico presentado  
- `README.md`: Este archivo

---

## Mi participación

Este trabajo fue realizado en parejas.  
Mi aporte principal fue diseñar y coordinar la lógica de sincronización entre los distintos hilos del sistema, asegurando que las acciones de **sentarse, servir, comer, responder y levantarse** se ejecutaran en el orden correcto y sin conflictos.  
Utilicé semáforos para gestionar el acceso a recursos compartidos y garantizar una experiencia concurrente controlada y realista.

---

## Posibles mejoras

- Reestructurar el código por **actores** (invitados, mozos, Manucho) en lugar de por momentos (sentarse, comer, levantarse).
- Crear funciones que agrupen toda la actividad de cada actor, en lugar de conectar acciones únicamente mediante semáforos, para mejorar la claridad y modularidad del código.

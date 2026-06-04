#include <stdlib.h>
#include <stdint.h>
#include <stdint.h>
#include <immintrin.h>
#include <stdio.h>  
#include <stdbool.h>
#include <pthread.h>
#include <string.h>
#include <time.h>



void fixedpoints(int maxkeys, int maxrounds);
void imprimiArreglo(int tam, unsigned char *in );
bool compare_m128i(__m128i a, __m128i b);
void write_fixedpoint_to_file(__m128i fixedpoint, int rounds, __m128i key, const char *filename);
void clear_fixedpoint_file(const char *filename);
void* fixedpoints_randoms_thread(void *arg);
static inline __m128i AES_Encrypt_rounds_static_keys(__m128i tmp, __m128i key, int rounds);

void fixedpoints_random_search(int max_points, int maxrounds);
typedef struct {
    int thread_id;
    int maxkeys;
    int max_points;
    int maxrounds;
    int num_threads;
} thread_args_t;

int main(int argc, char const *argv[])
{
    /* code */
    int maxkeys = 256; // Cambia este valor para probar con más o menos claves
    int maxrounds = 51;
    fixedpoints(maxkeys, maxrounds);
    // int max_points = 1; // Cambia este valor para probar con más o menos puntos aleatorios
    // fixedpoints_random_search(max_points, maxrounds);

    // __m128i test = _mm_set1_epi32(0x228db6c1);
    // __m128i key = _mm_setzero_si128();
    // test = AES_Encrypt_rounds_static_keys(test, key, 1088297794);
    // imprimiArreglo(16, (unsigned char *)&test);

    
    return 0;
}


void imprimiArreglo(int tam, unsigned char *in )
{

    for (int i = 0; i<tam; i++){
        printf("%02x", in[i] );
    }
    printf("\n" );

}


bool compare_m128i(__m128i a, __m128i b) {
    __m128i cmp = _mm_cmpeq_epi8(a, b);
    int mask = _mm_movemask_epi8(cmp);
    return mask == 0xFFFF;
}


void write_fixedpoint_to_file(__m128i fixedpoint, int rounds, __m128i key, const char *filename) {
    FILE *fp = fopen(filename, "a");
    
    if (fp == NULL) {
        perror("Error al abrir el fichero");
        return;
    }
    
    // Escribir el punto fijo en hexadecimal
    fprintf(fp, "Fixed Point: ");
    for (int i = 0; i < 16; i++) {
        fprintf(fp, "%02x", ((uint8_t *)&fixedpoint)[i]);
    }
    
    // Escribir el número de rondas en decimal
    fprintf(fp, " | Rounds: %d | Key: ", rounds);
    
    // Escribir la llave en hexadecimal
    for (int i = 0; i < 16; i++) {
        fprintf(fp, "%02x", ((uint8_t *)&key)[i]);
    }
    
    fprintf(fp, "\n");
    fclose(fp);
}


// Limpia el archivo de resultados dado
void clear_fixedpoint_file(const char *filename) {
    FILE *fp = fopen(filename, "w");
    
    if (fp == NULL) {
        perror("Error al abrir el fichero");
        return;
    }
    
    fclose(fp);
    printf("Archivo %s limpiado.\n", filename);
}


static inline __m128i AES_Encrypt_rounds_static_keys(__m128i tmp, __m128i key, int rounds){
	int j;
	// tmp = _mm_xor_si128 (tmp,key);
	for (j=1; j<rounds; j++)  tmp = _mm_aesenc_si128 (tmp,key);
	tmp = _mm_aesenc_si128 (tmp,key);
    return tmp;
}

void* fixedpoints_thread(void *arg) {
    thread_args_t *args = (thread_args_t *)arg;
    int thread_id = args->thread_id;
    int maxkeys = args->maxkeys;
    int maxrounds = args->maxrounds;
    int num_threads = args->num_threads;

    int keys_per_thread = maxkeys/ num_threads;
    
    // Calcular rango de claves para este hilo
    int start_key = (thread_id * keys_per_thread);
    int end_key = start_key + keys_per_thread;
    
    // Crear nombre del archivo para este hilo
    char filename[64];
    snprintf(filename, sizeof(filename), "fixed-point-thread-%d.txt", thread_id);
    clear_fixedpoint_file(filename);
    
    __m128i key = _mm_setzero_si128();
    
    for (int i = start_key; i < end_key; i++) {
        key = _mm_set1_epi8(i);
        for (size_t j = 0; j < UINT32_MAX; j++) {
            __m128i input_block = _mm_set1_epi32(j);
            __m128i output_block = _mm_set1_epi32(j);

            for (size_t k = 1; k < maxrounds; k++) {
    	        output_block = _mm_aesenc_si128 (output_block,key);
                bool is_fixed_point = compare_m128i(input_block, output_block);
                if (is_fixed_point) {
                    write_fixedpoint_to_file(input_block, k, key, filename);
                    break; // Salir del bucle de rondas si se encuentra un punto fijo
                }
            }
        }
    }
    
    free(args);
    return NULL;
}







void fixedpoints(int maxkeys, int maxrounds){
    int num_threads = 32;  // Cambiar este valor para usar más o menos hilos
    pthread_t threads[num_threads];
    
    printf("Iniciando búsqueda de puntos fijos con %d hilos\n", num_threads);
    
    // Crear los hilos
    for (int i = 0; i < num_threads; i++) {
        thread_args_t *args = (thread_args_t *)malloc(sizeof(thread_args_t));
        args->thread_id = i;
        args->maxkeys = maxkeys;
        args->maxrounds = maxrounds;
        args->num_threads = num_threads;
        
        pthread_create(&threads[i], NULL, fixedpoints_thread, args);
    }
    
    // Esperar a que terminen todos los hilos
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }
    
    printf("Búsqueda completada\n");
}


void fixedpoints_random_search(int max_points, int maxrounds){
    int num_threads = 1;  // Cambiar este valor para usar más o menos hilos
    pthread_t threads[num_threads];
    
    printf("Iniciando búsqueda de puntos fijos con %d hilos\n", num_threads);
    
    // Crear los hilos
    for (int i = 0; i < num_threads; i++) {
        thread_args_t *args = (thread_args_t *)malloc(sizeof(thread_args_t));
        args->thread_id = i;
        args->max_points = max_points;
        args->maxrounds = maxrounds;
        args->num_threads = num_threads;
        
        pthread_create(&threads[i], NULL, fixedpoints_randoms_thread, args);
    }
    
    // Esperar a que terminen todos los hilos
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }
    
    printf("Búsqueda completada\n");
}



void* fixedpoints_randoms_thread(void *arg) {
    thread_args_t *args = (thread_args_t *)arg;
    int thread_id = args->thread_id;
    int max_points = args->max_points;
    int maxrounds = args->maxrounds;
    int num_threads = args->num_threads;

    int keys_per_thread = max_points/ num_threads;
    // Calcular rango de claves para este hilo
    int start_key = (thread_id * keys_per_thread);
    int end_key = start_key + keys_per_thread;
    
    
    // Crear nombre del archivo para este hilo
    char filename[64];
    snprintf(filename, sizeof(filename), "fixed-point-random-thread-%d.txt", thread_id);
    clear_fixedpoint_file(filename);
    srand(time(NULL));   // Initialization, should only be called once.
    
    __m128i key = _mm_setzero_si128();
    
    key = _mm_set1_epi8(0);
    for (size_t j = start_key; j < end_key; j++) {
        sleep(j%11);
        int r1 = rand();      
        int r2 = rand();      
        int r3 = rand();      
        int r4 = rand();      
        printf("Thread %d: Punto aleatorio %zu: %08x \n", thread_id, j, r1);
        __m128i input_block = _mm_set_epi32(r1, r1, r1, r1);
        __m128i output_block = _mm_setzero_si128();
        imprimiArreglo(16, (unsigned char *)&input_block);

        // output_block = AES_Encrypt_rounds_static_keys(input_block, key, 1);
	    output_block = _mm_aesenc_si128 (input_block,key);

        for (size_t k = 0; k < UINT32_MAX; k++) {

	        output_block = _mm_aesenc_si128 (output_block,key);
            
            // if (k%10000 == 0){
                // printf("Thread %d: Ronda %zu: ", thread_id, k);
                // imprimiArreglo(16, (unsigned char *)&output_block);
            // }
            
            bool is_fixed_point = compare_m128i(input_block, output_block);
            if (is_fixed_point) {
                write_fixedpoint_to_file(input_block, k, key, filename);
                printf("Thread %d: Ronda %zu: \n", thread_id, k);
                imprimiArreglo(16, (unsigned char *)&output_block);
                imprimiArreglo(16, (unsigned char *)&input_block);
                break; // Salir del bucle de rondas si se encuentra un punto fijo
            }
        }
    }
    
    
    free(args);
    return NULL;
}

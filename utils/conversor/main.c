#include <stdio.h>
#include "converteutf832.h"

// Declaração das funções convUtf8p32 e convUtf32p8
int convUtf8p32(FILE *arquivo_entrada, FILE *arquivo_saida);
int convUtf32p8(FILE *arquivo_entrada, FILE *arquivo_saida);

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Uso: %s <arquivo_utf32> <arquivo_utf8>\n", argv[0]);
        return -1;
    }

    // Abre os arquivos de entrada e saída
    FILE *arquivo_entrada = fopen(argv[1], "rb");
    if (!arquivo_entrada) {
        fprintf(stderr, "Erro ao abrir o arquivo de entrada: %s\n", argv[1]);
        return -1;
    }

    FILE *arquivo_saida = fopen(argv[2], "wb");
    if (!arquivo_saida) {
        fprintf(stderr, "Erro ao criar o arquivo de saída: %s\n", argv[2]);
        fclose(arquivo_entrada);
        return -1;
    }

    // Converte de UTF-32 para UTF-8
    int resultado = convUtf32p8(arquivo_entrada, arquivo_saida);
    if (resultado != 0) {
        fprintf(stderr, "Erro na conversão de UTF-32 para UTF-8.\n");
    } else {
        printf("Conversão realizada com sucesso!\n");
    }

    // Fecha os arquivos
    fclose(arquivo_entrada);
    fclose(arquivo_saida);

    return resultado;
}

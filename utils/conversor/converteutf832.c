#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

#define BUFFER_SIZE 4096

int convUtf32p8(FILE *arquivo_entrada, FILE *arquivo_saida) {
    if (!arquivo_entrada || !arquivo_saida) {
        fprintf(stderr, "Erro com os arquivos.\n");
        return -1;
    }

    unsigned char buffer[BUFFER_SIZE];
    size_t bytes_read;

    while ((bytes_read = fread(buffer, 1, BUFFER_SIZE, arquivo_entrada)) > 0) {
        for (size_t i = 0; i < bytes_read; i++) {

            if (buffer[i] == 'B' && buffer[i + 1] == 'T') {
                fwrite("BT ", 1, 3, arquivo_saida);
                i += 2;

                while (i < bytes_read && !(buffer[i] == 'E' && buffer[i + 1] == 'T')) { // Até "ET"
                    uint32_t unicode = (buffer[i] << 24) | (buffer[i + 1] << 16) |
                                       (buffer[i + 2] << 8) | buffer[i + 3];
                    i += 4;

                    if (unicode <= 0x7F) {
                        fputc(unicode, arquivo_saida);
                    } else if (unicode <= 0x7FF) {
                        fputc(0xC0 | (unicode >> 6), arquivo_saida);
                        fputc(0x80 | (unicode & 0x3F), arquivo_saida);
                    } else if (unicode <= 0xFFFF) {
                        fputc(0xE0 | (unicode >> 12), arquivo_saida);
                        fputc(0x80 | ((unicode >> 6) & 0x3F), arquivo_saida);
                        fputc(0x80 | (unicode & 0x3F), arquivo_saida);
                    } else if (unicode <= 0x10FFFF) {
                        fputc(0xF0 | (unicode >> 18), arquivo_saida);
                        fputc(0x80 | ((unicode >> 12) & 0x3F), arquivo_saida);
                        fputc(0x80 | ((unicode >> 6) & 0x3F), arquivo_saida);
                        fputc(0x80 | (unicode & 0x3F), arquivo_saida);
                    } else {
                        fprintf(stderr, "Caractere inválido no texto.\n");
                        return -1;
                    }
                }

                fwrite("ET ", 1, 3, arquivo_saida);
                i += 2;
            } else {
                fputc(buffer[i], arquivo_saida);
            }
        }
    }

    return 0;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <arquivo_entrada>\n", argv[0]);
        return 1;
    }

    const char *arquivo_entrada_path = argv[1];

    char arquivo_saida_path[256];
    snprintf(arquivo_saida_path, sizeof(arquivo_saida_path), "_database/reports/%s", arquivo_entrada_path);
    char *ext = strstr(arquivo_saida_path, "_utf32");
    if (ext) {
        strcpy(ext, "_utf8.pdf");
    } else {
        fprintf(stderr, "Nome do arquivo de entrada não está no formato esperado.\n");
        return 1;
    }

    FILE *arquivo_entrada = fopen(arquivo_entrada_path, "rb");
    if (!arquivo_entrada) {
        fprintf(stderr, "Erro ao abrir arquivo de entrada: %s\n", arquivo_entrada_path);
        return 1;
    }

    FILE *arquivo_saida = fopen(arquivo_saida_path, "wb");
    if (!arquivo_saida) {
        fprintf(stderr, "Erro ao criar arquivo de saída: %s\n", arquivo_saida_path);
        fclose(arquivo_entrada);
        return 1;
    }

    int result = convUtf32p8(arquivo_entrada, arquivo_saida);

    fclose(arquivo_entrada);
    fclose(arquivo_saida);

    if (result != 0) {
        fprintf(stderr, "Erro ao converter o arquivo.\n");
        return 1;
    }

    if (!remove(arquivo_entrada_path) == 0) {
        fprintf(stderr, "Erro ao remover o arquivo original: %s\n", arquivo_entrada_path);
    }
    return 0;
}

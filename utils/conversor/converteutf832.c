/* Rafael Dana Christof 2410977 3WA */

#include <stdio.h>
#include "converteutf832.h"

int convUtf32p8(FILE *arquivo_entrada, FILE *arquivo_saida) {
    if (!arquivo_entrada || !arquivo_saida) {
        fprintf(stderr, "Erro com os arquivos.\n");
        return -1;
    }

    unsigned char bom[4];
    if (fread(bom, sizeof(unsigned char), 4, arquivo_entrada) != 4) {
        fprintf(stderr, "A leitura do arquivo falhou.\n");
        return -1;
    }

    int little_endian = 0;
    if (bom[0] == 0xFF && bom[1] == 0xFE && bom[2] == 0x00 && bom[3] == 0x00) {
        little_endian = 1;
    } else if (bom[0] == 0x00 && bom[1] == 0x00 && bom[2] == 0xFE && bom[3] == 0xFF) {
        little_endian = 0;
    } else {
        fprintf(stderr, "bom invalido.\n");
        return -1;
    }

    unsigned int unicode;
    while (fread(&unicode, sizeof(unsigned int), 1, arquivo_entrada) == 1) {
        if (!little_endian) {
            unicode = (unicode >> 24) |
                      ((unicode << 8) & 0x00FF0000) |
                      ((unicode >> 8) & 0x0000FF00) |
                      (unicode << 24);
        }
        
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
            fprintf(stderr, "unicode invalido.\n");
            return -1;
        }
    }

    return 0;
}
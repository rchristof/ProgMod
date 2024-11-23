/* Rafael Dana Christof 2410977 3WA */

#include <stdio.h>
#include "converteutf832.h"

int convUtf8p32(FILE *arquivo_entrada, FILE *arquivo_saida) {
    if (!arquivo_entrada || !arquivo_saida) {
        fprintf(stderr, "Erro com os arquivos.\n");
        return -1;
    }

    unsigned char bom[] = {0xFF, 0xFE, 0x00, 0x00};
    if (fwrite(bom, sizeof(unsigned char), 4, arquivo_saida) != 4) {
        fprintf(stderr, "A escrita no arquivo falhou.\n");
        return -1;
    }

    int byte;
    while ((byte = fgetc(arquivo_entrada)) != EOF) {
        unsigned int unicode = 0;

        if (byte <= 0x7F) unicode = byte;
        else if ((byte & 0xE0) == 0xC0) {
            int byte2 = fgetc(arquivo_entrada);
            if (byte2 == EOF) {
                fprintf(stderr, "A leitura do arquivo falhou.\n");
                return -1;
            }
            unicode = ((byte & 0x1F) << 6) | (byte2 & 0x3F);
        } else if ((byte & 0xF0) == 0xE0) {
            int byte2 = fgetc(arquivo_entrada);
            int byte3 = fgetc(arquivo_entrada);
            if (byte2 == EOF || byte3 == EOF) {
                fprintf(stderr, "A leitura do arquivo falhou.\n");
                return -1;
            }
            unicode = ((byte & 0x0F) << 12) |
                             ((byte2 & 0x3F) << 6) |
                             (byte3 & 0x3F);
        } else if ((byte & 0xF8) == 0xF0) {
            int byte2 = fgetc(arquivo_entrada);
            int byte3 = fgetc(arquivo_entrada);
            int byte4 = fgetc(arquivo_entrada);
            if (byte2 == EOF || byte3 == EOF || byte4 == EOF) {
                fprintf(stderr, "A leitura do arquivo falhou.\n");
                return -1;
            }
            unicode = ((byte & 0x07) << 18) |
                             ((byte2 & 0x3F) << 12) |
                             ((byte3 & 0x3F) << 6) |
                             (byte4 & 0x3F);
        } else {
            fprintf(stderr, "Caractere invalido.\n");
            return -1;
        }

        int confirma = fwrite(&unicode, sizeof(unsigned int), 1, arquivo_saida);
        if (confirma != 1) {
            fprintf(stderr, "Erro de escrita no arquivo.\n");
            return -1;
        }
    }

    return 0;
}


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


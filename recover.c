#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{

    // error check to ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Try Usage: ./recover image\n");
        return 1;
    }

    // try to open a file and check if the file is valid
    char *file1 = argv[1];
    FILE *filepointer = fopen(file1, "r");
    if (filepointer == NULL)
    {
        fprintf(stderr, "File %s cannot be opened.\n", file1);
        return 2;
    }

    unsigned char *buff = malloc(512);
    int jpgnum = 0;
    FILE *image;

    while (fread(buff, 512, 1, filepointer))
    {
        // find new jpg file
        if (buff[0] == 0xff && buff[1] == 0xd8 && buff[2] == 0xff && (buff[3] & 0xf0) == 0xe0)
        {
            // exit last jpeg file
            if (jpgnum > 0)
            {
                fclose(image);
            }

            // make filename
            char filename[7];
            sprintf(filename, "%03i.jpg", jpgnum);

            // open processed jpg file
            image = fopen(filename, "w");

            // check what was created
            if (image == NULL)
            {
                fclose(filepointer);
                free(buff);
                fprintf(stderr, "JPG %s could not be created.", filename);
                return 3;
            }

            jpgnum++;
        }

        // if jpg not found, skip
        if (!jpgnum)
        {
            continue;
        }

        // write jpg bits into the new created jpg
        fwrite(buff, 512, 1, image);
    }

    fclose(filepointer);
    fclose(image);

    free(buff);

    return 0;
}
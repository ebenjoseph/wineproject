/**
 * File: superscript.c
 * Author: Eli Ben-Joseph
 * -----------
 * A simple script to take in wine flavor inputs, process them,
 * run through mallet, and print the outputs.
 */

#include <stdbool.h>       // for bool type
#include <stdio.h>         // for printf, etc
#include <stdlib.h>        
#include <unistd.h>        // for fork
#include <string.h>        // for strlen, strcasecmp, etc
#include <ctype.h>
#include <signal.h>        // for signal
#include <sys/types.h>
#include <sys/wait.h>      // for wait, waitpid
#include <errno.h>
#include <fcntl.h>

 int main(int argc, char *argv[]) {

 	// shell commands to be executed
 	char *command1 = "cat ./data/inputfile.txt | python ngram_format.py > data/inputfile2.txt";
 	char *command2 = "bin/mallet classify-file --input data/inputfile2.txt --output tempoutput.txt --classifier wine_5k.classifier.trial0";  // command line to be executed
 	char *command3 = "cat tempoutput.txt | python outputsorter.py";
 	
 	char i[2000];  // input buffer

 	// read in words
 	fgets(i, sizeof i, stdin);
	printf("your input: %s\n", i);

	FILE *fp = fopen("./data/inputfile.txt", "w+");
    if (fp != NULL)
    {
        fputs(i, fp);
        fclose(fp);
    }

    system(command1);  // run python stemmer

    FILE *fp2 = fopen("./data/inputfile2.txt", "r+");
    if (fp2 != NULL)
    {
        fputs("blank ", fp2); // add in blank word for mallet format
        fclose(fp2);
    }

    system(command2);  // run mallet script
    system(command3);  // run python sorter

 	return 0;
 }

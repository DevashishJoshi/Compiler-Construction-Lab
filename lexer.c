#include<stdio.h>
#include <stdlib.h>

int isEqualstr(char a[10],char b[10]){
	int i=0;
	while(i<10&&a[i]&&b[i]){
		if(a[i]!=b[i]) return 0;
		i++;
	}
	return 1;
}

int iskeyword(char word[10], int len){
	int i;
	char keywords[4][10]={"printf", "void", "main", "int"};
	for(i=0;i<4;i++)
		if(isEqualstr(keywords[i],word)) return 1;
	
	return 0;
}

void main(){

    FILE *fptr;
    char filename[15]="helloworld.c", ch;
    
    fptr = fopen(filename, "r");
	ch = fgetc(fptr);
	
	while(ch != EOF ){
		switch(ch){
			case ' ' :  break;
			case '/' :  ch = fgetc(fptr);
						// Check if it is a comment
						if(ch == '/'){ // single line comment
							printf("Single line comment : ");
							while(ch != '\n'){ // skip all chars upto new line						
								ch = fgetc(fptr);
								printf("%c", ch);
							}
							//printf("\n");
						}
						else if(ch == '*'){ // multi line comment
							printf("Multi line comment : ");
							while(1){ // skip all chars upto */
								if(ch != '*'){
									printf("%c", ch);								
									ch = fgetc(fptr);
								}								
								else{
									ch = fgetc(fptr);
									if(ch == '/')
										break;						
								}
							}
						}
						break;
			case '#' :  printf("Preprocessor directive : ");
						while(ch != '\n'){
							printf("%c", ch);							
							ch = fgetc(fptr);							
						}
						printf("\n");
						break;
			case '\'' : ch = fgetc(fptr);
						printf("Character literal : "); ch = fgetc(fptr); printf("%c\n", ch);
						break;
			case '\"' :	printf("String literal : "); ch = fgetc(fptr); while(ch != '\"'){ printf("%c", ch); ch = fgetc(fptr); } printf("\n"); break;

			default : 	// check if ch is a digit
						if(isdigit(ch)) { printf("Number"); while(isdigit(ch) || ch =='.') { printf("%c", ch); ch = fgetc(fptr); } printf("\n"); }
						// check if ch is an keyword / identifier
						else if(isalpha(ch)){
							char word[10];
							int i=0;
							while(i<10 && isalpha(ch)){
								word[i++] = ch;
								ch = fgetc(fptr);
							}
							word[i]=0;

							if(iskeyword(word, i))
								printf("Keyword : %s", word);							
							
							else
								printf("Identifier : %s", word);								
							
							printf("\n");
						}
		}
		ch = fgetc(fptr);
	}
    fclose(fptr);
}
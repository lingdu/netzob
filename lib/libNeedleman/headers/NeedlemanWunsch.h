#ifndef __NeedlemanWunsch_header
#define __NeedlemanWunsch__header

#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>


/**
 * Definitions of the different ENUM
 */

typedef enum {
	FALSE, TRUE
} BOOL;

typedef struct {
	unsigned short int len; // length of the message
	char *message; // a message
} t_message;

typedef struct {
	unsigned short int len; // nb of messages in the group
	t_message *messages; // a list of messages
} t_group;

typedef struct {
	unsigned short int len; // size of the regex
	char *regex; // the actual regex
	char *mask; // its mask
	float score;
} t_regex;




static PyObject* py_getMatrix(PyObject* self, PyObject* args);

void initlibNeedleman();
void alignTwoSequences(t_regex seq1, t_regex seq2, t_regex *regex);
int hexdump(unsigned char *buf, int dlen);


/**
 * Bind Python function names to our C functions
 */
static PyMethodDef libNeedleman_methods[] = {
	{"getMatrix", py_getMatrix, METH_VARARGS},
	{NULL, NULL}
};
#endif
// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

unsigned int word_count = 0;

bool loaded = false;

int hash_it(char *needs_hashing)
{
    unsigned int hash = 0;
    for (int i = 0, n = strlen(needs_hashing); i < n; i++)
    {
        hash = (hash << 2) ^ needs_hashing[i];
    }
    return hash % N;
}

bool check(const char *word)
{
    int len = strlen(word);
    char word_copy[len + 1];

    for (int i = 0; i < len; i++)
    {
        word_copy[i] = tolower(word[i]);
    }


    word_copy[len] = '\0';

    int h = hash_it(word_copy);


    node *cursor = hashtable[h];


    while (cursor != NULL)
    {
        if (strcmp(cursor->word, word_copy) == 0)
        {

            return true;
        }
        else
        {

            cursor = cursor->next;
        }
    }
    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *fp = fopen(dictionary, "r");
    if (fp == NULL)
    {
        printf("Unable to open dictionary.\n");
        return false;
    }
    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (true)
    {

        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            printf("Unable to Malloc.\n");
            return false;
        }


        fscanf(fp, "%s", new_node->word);
        new_node->next = NULL;

        if (feof(fp))
        {
            free(new_node);
            break;
        }

        word_count++;


        int h = hash_it(new_node->word);
        node *head = hashtable[h];


        if (head == NULL)
        {
            hashtable[h] = new_node;
        }
        else
        {
            new_node->next = hashtable[h];
            hashtable[h] = new_node;
        }
    }
    // Close dictionary
    fclose(fp);
    loaded = true;
    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (loaded)
    {
        return word_count;
    }
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = hashtable[i];
        while (cursor != NULL)
        {
            // maintain connection to linked list using temp
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    loaded = false;
    return true;
}
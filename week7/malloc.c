//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *free_head;
  size_t upper_bound;
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
const int  BIN_NUM = 4;
my_heap_t my_heap[BIN_NUM];

//
// Helper functions (feel free to add/remove/edit!)
//

int find_bin(size_t size) {
  for (int i = 0; i < BIN_NUM; i++) {
    if (size <= my_heap[i].upper_bound) 
      return i;
  }
  return BIN_NUM - 1; // fallback to largest bin
}

void my_add_to_free_list(my_metadata_t *metadata, int heap_idx) {
  assert(!metadata->next);
  metadata->next = my_heap[heap_idx].free_head;
  my_heap[heap_idx].free_head = metadata;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev, int heap_idx) {
  if (prev) {
    prev->next = metadata->next;
  } else {
    my_heap[heap_idx].free_head = metadata->next;
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  my_heap[0].upper_bound = 1000;
  my_heap[1].upper_bound = 2000;
  my_heap[2].upper_bound = 3000;
  my_heap[3].upper_bound = 4096;
  for (int i = 0; i < BIN_NUM; i++) {
    my_heap[i].free_head = NULL;
  }
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {
  while (1) {
    int heap_idx = find_bin(size);
    my_metadata_t *best = NULL;
    my_metadata_t *best_prev = NULL;
    int best_idx = -1;
    my_metadata_t *prev = NULL;
    my_metadata_t *current = NULL;

    for (int i = heap_idx; i < BIN_NUM; i++) {
      prev = NULL;
      current = my_heap[i].free_head;
      while (current) {
        if (current->size >= size) {
          if (!best || current->size < best->size) {
            best = current;
            best_prev = prev;
            best_idx = i;
          }
        }
        prev = current;
        current = current->next;
      }
      if (best) break;
    }

    if (!best) {
      size_t buffer_size = 4096;
      my_metadata_t *new_block = (my_metadata_t *)mmap_from_system(buffer_size);
      new_block->size = buffer_size - sizeof(my_metadata_t);
      new_block->next = NULL;
      my_add_to_free_list(new_block, find_bin(new_block->size));
      continue;
    }

    void *ptr = best + 1;
    size_t remaining = best->size - size;
    my_remove_from_free_list(best, best_prev, best_idx);

    if (remaining > sizeof(my_metadata_t)) {
      best->size = size;
      my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
      new_metadata->size = remaining - sizeof(my_metadata_t);
      new_metadata->next = NULL;
      my_add_to_free_list(new_metadata, find_bin(new_metadata->size));
    }

    return ptr;
  }
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  int heap_idx = find_bin(metadata->size);
  my_add_to_free_list(metadata, heap_idx);
}


// This is called at the end of each challenge.
void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}

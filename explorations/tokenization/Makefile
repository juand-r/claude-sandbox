# Makefile for tokenization experiment
#
# Builds 5 binaries from train_tok.c, each with a different TOKENIZE_MODE.
# Links against the QAT-CPU library objects from ../qat-cpu.

QAT_DIR := ../qat-cpu

CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2 -g -D_GNU_SOURCE -fopenmp -I$(QAT_DIR)
LDFLAGS = -lm -fopenmp

# QAT library object files
QAT_OBJ := $(QAT_DIR)/memory.o $(QAT_DIR)/cpu_detect.o $(QAT_DIR)/kernels_scalar.o \
            $(QAT_DIR)/quantize.o $(QAT_DIR)/dispatch.o $(QAT_DIR)/qat_linear.o \
            $(QAT_DIR)/layers.o $(QAT_DIR)/optimizer.o $(QAT_DIR)/loss.o \
            $(QAT_DIR)/kernels_avx2.o $(QAT_DIR)/kernels_vnni.o $(QAT_DIR)/kernels_bf16.o

.PHONY: all clean qat_lib data

all: qat_lib data train_tok_binary train_tok_base4 train_tok_nibble train_tok_char train_tok_bigram

# Build QAT library objects
qat_lib:
	$(MAKE) -C $(QAT_DIR) $(notdir $(QAT_OBJ))

# Symlink data file
data: shakespeare.txt
shakespeare.txt:
	ln -sf $(QAT_DIR)/shakespeare.txt .

# Five tokenization mode binaries
# TRAIN_CFLAGS allows override: make TRAIN_CFLAGS="-DDIM=256 -DN_STEPS=5000"

train_tok_binary: train_tok.c $(QAT_OBJ)
	$(CC) $(CFLAGS) $(TRAIN_CFLAGS) -DTOKENIZE_MODE=0 $< $(QAT_OBJ) -o $@ $(LDFLAGS)

train_tok_base4: train_tok.c $(QAT_OBJ)
	$(CC) $(CFLAGS) $(TRAIN_CFLAGS) -DTOKENIZE_MODE=1 $< $(QAT_OBJ) -o $@ $(LDFLAGS)

train_tok_nibble: train_tok.c $(QAT_OBJ)
	$(CC) $(CFLAGS) $(TRAIN_CFLAGS) -DTOKENIZE_MODE=2 $< $(QAT_OBJ) -o $@ $(LDFLAGS)

train_tok_char: train_tok.c $(QAT_OBJ)
	$(CC) $(CFLAGS) $(TRAIN_CFLAGS) -DTOKENIZE_MODE=3 $< $(QAT_OBJ) -o $@ $(LDFLAGS)

train_tok_bigram: train_tok.c $(QAT_OBJ)
	$(CC) $(CFLAGS) $(TRAIN_CFLAGS) -DTOKENIZE_MODE=4 $< $(QAT_OBJ) -o $@ $(LDFLAGS)

# Factored embedding sweep
sweep_factored: qat_lib data
	./sweep_factored.sh

clean:
	rm -f train_tok_binary train_tok_base4 train_tok_nibble train_tok_char train_tok_bigram
	rm -f *.csv *_output.txt
	rm -rf factored_results

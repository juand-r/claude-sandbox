# Makefile for QAT-CPU
#
# Build system with per-ISA compilation flags.
# Each kernel file gets its own flags so the compiler can use
# the right instructions without affecting other translation units.

CC = gcc
CFLAGS_BASE = -std=c11 -Wall -Wextra -O2 -g -D_GNU_SOURCE -fopenmp
LDFLAGS = -lm -fopenmp

# ISA-specific flags
CFLAGS_SCALAR = $(CFLAGS_BASE)
CFLAGS_AVX2   = $(CFLAGS_BASE) -mavx2 -mfma
CFLAGS_VNNI   = $(CFLAGS_BASE) -mavx512f -mavx512bw -mavx512vnni -mavx512vl

# Source files grouped by ISA requirement
SRC_SCALAR = memory.c cpu_detect.c kernels_scalar.c quantize.c \
             dispatch.c qat_linear.c layers.c optimizer.c loss.c
SRC_AVX2   = kernels_avx2.c
SRC_VNNI   = kernels_vnni.c

# Object files
OBJ_SCALAR = $(SRC_SCALAR:.c=.o)
OBJ_AVX2   = $(SRC_AVX2:.c=.o)
OBJ_VNNI   = $(SRC_VNNI:.c=.o)
OBJ_ALL    = $(OBJ_SCALAR) $(OBJ_AVX2) $(OBJ_VNNI)

# Targets
.PHONY: all test bench train clean

all: test_qat train_qat

# Compilation rules by ISA
$(OBJ_SCALAR): %.o: %.c qat_cpu.h
	$(CC) $(CFLAGS_SCALAR) -c $< -o $@

$(OBJ_AVX2): %.o: %.c qat_cpu.h
	$(CC) $(CFLAGS_AVX2) -c $< -o $@

$(OBJ_VNNI): %.o: %.c qat_cpu.h
	$(CC) $(CFLAGS_VNNI) -c $< -o $@

# Test binary
test_main.o: test_main.c qat_cpu.h
	$(CC) $(CFLAGS_SCALAR) -c $< -o $@

test_qat: test_main.o $(OBJ_ALL)
	$(CC) $^ -o $@ $(LDFLAGS)

# Training binary
train.o: train.c qat_cpu.h
	$(CC) $(CFLAGS_SCALAR) -c $< -o $@

train_qat: train.o $(OBJ_ALL)
	$(CC) $^ -o $@ $(LDFLAGS)

# Run tests
test: test_qat
	./test_qat

# Run training
train: train_qat
	./train_qat

clean:
	rm -f *.o test_qat train_qat

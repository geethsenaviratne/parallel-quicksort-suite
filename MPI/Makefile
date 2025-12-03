# Makefile for MPI Parallel QuickSort
# File: quicksort_mpi.c

SHELL := /bin/bash

# MPI compiler
CC := mpicc

# Compiler flags
CFLAGS := -O3 -Wall

# Linker flags (if needed)
LDFLAGS :=

# Target executable
TARGET := quicksort_mpi

# Source file
SRC := quicksort_mpi.c

# Default mpirun (override with MPIRUN=... on make cmdline)
MPIRUN ?= mpirun

.PHONY: all clean run test eval help

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC) $(LDFLAGS)
	@echo "Compilation successful!"
	@echo "Run with: $(MPIRUN) -np <procs> ./$(TARGET) <array_size>"

clean:
	@rm -f $(TARGET)
	@echo "Cleaned up!"

# Interactive run: prompts for PROCS and ARRAY (defaults: 4 procs, 1000000 elements).
# Also supports non-interactive invocation:
#   make run PROCS=8 ARRAY=1000000
run:
	@if [ ! -x ./$(TARGET) ]; then \
	  echo "Executable not found. Building..."; \
	  $(MAKE) $(TARGET); \
	fi; \
	if [ -n "$(PROCS)" ]; then \
	  procs="$(PROCS)"; \
	else \
	  read -p "Enter number of processes [1, 2, 4, 8]: " procs; \
	  procs=$${procs:-4}; \
	fi; \
	if [ -n "$(ARRAY)" ]; then \
	  arr="$(ARRAY)"; \
	else \
	  read -p "Enter array size [1000000]: " arr; \
	  arr=$${arr:-1000000}; \
	fi; \
	echo "Running: $(MPIRUN) -np $$procs ./$(TARGET) $$arr"; \
	$(MPIRUN) -np $$procs ./$(TARGET) $$arr

# Quick non-interactive tests (1,2,4,8 procs) with 1M elements
test:
	@echo "Testing with 1 process..."
	$(MPIRUN) -np 1 ./$(TARGET) 10000000 || true
	@echo ""
	@echo "Testing with 2 processes..."
	$(MPIRUN) -np 2 ./$(TARGET) 10000000 || true
	@echo ""
	@echo "Testing with 4 processes..."
	$(MPIRUN) -np 4 ./$(TARGET) 10000000 || true
	@echo ""
	@echo "Testing with 8 processes..."
	$(MPIRUN) -np 8 ./$(TARGET) 10000000 || true


help:
	@echo "Available targets:"
	@echo "  make          - Compile the program"
	@echo "  make clean    - Remove executable"
	@echo "  make run      - Interactive run (prompts for PROCS and ARRAY)."
	@echo "                  Or non-interactive: make run PROCS=4 ARRAY=1000000"
	@echo "  make test     - Quick tests with several process counts"
	@echo "  make help     - Show this help"

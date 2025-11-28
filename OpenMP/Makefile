# Makefile for OpenMP Parallel QuickSort
# Author: IT23226128
# Course: SE3082 - Parallel Computing

# Compiler
CC = gcc

# Compiler flags
CFLAGS = -O3 -Wall -fopenmp

# Target executable
TARGET = quicksort_omp

# Source file
SRC = quicksort_omp.c

# Default target
all: $(TARGET)

# Build target
$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)
	@echo "Compilation successful!"
	@echo "Run with: ./$(TARGET) <array_size> <num_threads>"

# Clean target
clean:
	rm -f $(TARGET)
	@echo "Cleaned up!"

# Run with default settings
run:
	@# If user passed THREADS on the make command line, use it; otherwise prompt
	@if [ -n "$(THREADS)" ]; then \
	  threads="$(THREADS)"; \
	else \
	  read -p "Enter number of threads [1,2,4,8,16]: " threads; \
	  threads=$${threads:-4}; \
	fi; \
	echo "Running with $$threads threads..."; \
	./$(TARGET) 10000000 $$threads


# Test with different thread counts
test:
	@echo "Testing with 1 thread..."
	./$(TARGET) 1000000 1
	@echo ""
	@echo "Testing with 2 threads..."
	./$(TARGET) 1000000 2
	@echo ""
	@echo "Testing with 4 threads..."
	./$(TARGET) 1000000 4
	@echo ""
	@echo "Testing with 8 threads..."
	./$(TARGET) 1000000 8

	@echo "Testing with 16 threads..."
	./$(TARGET) 1000000 16

# Performance evaluation
eval:
	@echo "=== Performance Evaluation ==="
	@echo "1 thread:"
	./$(TARGET) 10000000 1
	@echo ""
	@echo "2 threads:"
	./$(TARGET) 10000000 2
	@echo ""
	@echo "4 threads:"
	./$(TARGET) 10000000 4
	@echo ""
	@echo "8 threads:"
	./$(TARGET) 10000000 8
	@echo ""
	@echo "16 threads:"
	./$(TARGET) 10000000 16

# Help
help:
	@echo "Available targets:"
	@echo "  make          - Compile the program"
	@echo "  make clean    - Remove executable"
	@echo "  make run      - Run with 1M elements, 4 threads"
	@echo "  make test     - Test with different thread counts"
	@echo "  make eval     - Full performance evaluation"
	@echo "  make help     - Show this help"
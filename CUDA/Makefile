# Makefile for CUDA Quick Sort (Custom Implementation)
# Author: IT23226128
# Course: SE3082 - Parallel Computing

# CUDA Compiler
NVCC = nvcc

# Compiler flags
NVCCFLAGS = -O3 -arch=sm_89

# Target executable
TARGET = cuda_quicksort

# Source file
SRC = cuda_quicksort.cu

# Default target
all: $(TARGET)

# Build target
$(TARGET): $(SRC)
	$(NVCC) $(NVCCFLAGS) -o $(TARGET) $(SRC)
	@echo "Compilation successful!"
	@echo "Run with: ./$(TARGET)"

# Clean target
clean:
	rm -f $(TARGET)
	@echo "Cleaned up!"

# Run with default settings
run:
	./$(TARGET)

# Help
help:
	@echo "Available targets:"
	@echo "  make          - Compile the program"
	@echo "  make clean    - Remove executable"
	@echo "  make run      - Run the program"
	@echo "  make help     - Show this help"

.PHONY: all clean run help

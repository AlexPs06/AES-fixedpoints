# CC=g++
# CFLAGS= -march=native 
# LIB= -O3 
# SOURCES= CPB.cpp
# all: 
# 	$(CC) -o test $(SOURCES) $(LIB) $(CFLAGS) 
# clean: 
# 	rm *.o  

# CC=g++
# CFLAGS= -march=armv8-a+crypto
# LIB= -Os 
# SOURCES= CPB_V2.cpp
# SOURCES2= ParaHash-V3.cpp
# all: 
# 	$(CC) -o CPB $(SOURCES) $(SOURCES2)  $(LIB) $(CFLAGS) 
# clean: 
# 	rm *.o  


# Compiler
CC := gcc

# Target
TARGET := test

# Source files
SRCS := fixedpoints.c

# Header files (for dependency tracking)
HDRS :=

# Compiler flags
CFLAGS := -O3 -march=native \
            -Wall -Wextra -Wno-unused-parameter

# Linker flags (empty but kept for clarity)
LDFLAGS := -lpthread

# Default rule
all: $(TARGET)

# Link
$(TARGET): $(SRCS) $(HDRS)
	$(CC) $(CFLAGS) $(SRCS) -o $(TARGET) $(LDFLAGS)

# Clean
clean:
	rm -f $(TARGET)

.PHONY: all clean

# general Makefile for simple projects
#
# 
  


TARGET=testcpp

CC=g++
FLAGS_C=-ggdb3 -O0 -Wall -std=c++11 -c -MMD -MP


SRCS=$(wildcard *.cpp)
OBJS=$(SRCS:.cpp=.o)
OBJD=$(SRCS:.cpp=.d)


$(TARGET): $(OBJS) 
	$(CC) -o $(TARGET) $(OBJS)


-include $(OBJD)				


$(OBJS): %.o: %.cpp
	$(CC) $(FLAGS_C) $<


cl:
	@-rm -rf $(TARGET) $(OBJS) $(OBJD)


show:
	@echo $(SRCS)
	@echo $(OBJD)
	@echo $(OBJS)

.PHONY: cl show

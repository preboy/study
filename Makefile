# general Makefile for simple projects
#
#
# 
# 
#  
# 
  

TARGET=testcpp

CC=g++
FLAGS_C=-ggdb -O0 -Wall -std=c++11 -c
FLAGS_D=-c -std=c++11 -MMD


SRCS=$(wildcard *.cpp)
OBJS=$(SRCS:.cpp=.o)
OBJD=$(SRCS:.cpp=.d)


target: $(OBJS) 
	$(CC) -o  $(TARGET) $(OBJS)


-include $(OBJD)	


cl:
	@-rm -rf $(TARGET) $(OBJS) $(OBJD)


show:
	@echo $(SRCS)


.PHONY: cl show

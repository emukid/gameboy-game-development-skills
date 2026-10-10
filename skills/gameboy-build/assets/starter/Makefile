GBDK_HOME ?= /opt/gbdk
LCC = $(GBDK_HOME)/bin/lcc
SOURCES := $(wildcard src/*.c)
HEADERS := $(wildcard src/*.h)
ROM := build/game.gb

.PHONY: all clean
all: $(ROM)

$(ROM): $(SOURCES) $(HEADERS) Makefile
	mkdir -p build
	"$(LCC)" -Wm-ynFORGE -Wm-yt0 -Wm-yo2 -Wl-m -Wl-j -o "$@" $(SOURCES)

clean:
	rm -rf build

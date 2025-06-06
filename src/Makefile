OBJECTS = creature.o dod.o dodgame.o dungeon.o enhanced.o object.o oslink.o parser.o player.o sched.o viewer.o

CXXFLAGS = -std=c++11 -c
# Add Homebrew paths for Apple Silicon Macs
ifeq ($(shell uname -m),arm64)
CXXFLAGS += -I/opt/homebrew/include
LDFLAGS += -L/opt/homebrew/lib
endif
ifdef EMSCRIPTEN
#CCLINK  = -s USE_SDL=2 -O3 -s USE_SDL_MIXER=2 -s USE_REGAL=1 -s ALLOW_MEMORY_GROWTH=1 --preload-file ../assets@/ -s FULL_ES2=1 -s ASYNCIFY -s WASM=1 -s EXIT_RUNTIME=1

ifdef WEBSITE
OUTPUT  = ../../index.js
CCLINK  = -s USE_SDL=2 -O3 -s USE_SDL_MIXER=2 -s USE_REGAL=1 -s ALLOW_MEMORY_GROWTH=1 --preload-file ../assets@/ -s FULL_ES2=1 -s ASYNCIFY -s WASM=1 -s EXIT_RUNTIME=1 -s EXPORTED_FUNCTIONS='["_sendinput", "_stopdemo", "_getinventory","_getfloor", "_main"]' -s EXTRA_EXPORTED_RUNTIME_METHODS='["ccall", "cwrap"]'
else
OUTPUT  = ../docs/index.html
CCLINK  = -s USE_SDL=2 -O3 -s USE_SDL_MIXER=2 -s USE_REGAL=1 -s ALLOW_MEMORY_GROWTH=1 --preload-file ../assets@/ -s FULL_ES2=1 -s ASYNCIFY -s WASM=1 -s EXIT_RUNTIME=1 --shell-file standalone.html
endif

#CCLINK  = -s USE_SDL=2 -O3 -s USE_SDL_MIXER=2 -s USE_REGAL=1 -s ALLOW_MEMORY_GROWTH=1 --preload-file ../assets@/ -s FULL_ES2=1 -s ASYNCIFY -s WASM=1 -s EXIT_RUNTIME=1 --shell-file template.html
CXXFLAGS += -O3 -s USE_SDL=2 -s USE_SDL_MIXER=2 -s USE_REGAL=1 -s ALLOW_MEMORY_GROWTH=1 -s FULL_ES2=1 -s ASYNCIFY -s WASM=1 -s EXIT_RUNTIME=1 
#CXX      = clang++-3.6
else
ifeq ($(OS),Windows_NT)
OUTPUT  = ../dod.exe
CCLINK  = -lopengl32 -lmingw32 -lSDL2main -lSDL2 -mwindows -lSDL2_mixer
else
OUTPUT  = ../dod
ifeq ($(shell uname),Darwin)
CCLINK  = -framework OpenGL -lSDL2 -lSDL2_mixer
else
CCLINK  = -lGL -lSDL2 -lSDL2_mixer
endif
endif
endif
#RM = rm
# -g is debug

all: $(OUTPUT)

$(OUTPUT): $(OBJECTS)
	$(CXX) $(LDFLAGS) -o $(OUTPUT) $(OBJECTS) $(CCLINK)

creature.o: creature.cpp creature.h dod.h
	$(CXX) $(CXXFLAGS) creature.cpp

dod.o: dod.cpp dod.h dodgame.h player.h object.h creature.h dungeon.h sched.h viewer.h oslink.h parser.h
	$(CXX) $(CXXFLAGS) dod.cpp

dodgame.o: dodgame.cpp dodgame.h player.h object.h viewer.h sched.h creature.h parser.h dungeon.h oslink.h dod.h
	$(CXX) $(CXXFLAGS) dodgame.cpp

dungeon.o: dungeon.cpp dungeon.h dodgame.h player.h sched.h dod.h
	$(CXX) $(CXXFLAGS) dungeon.cpp

enhanced.o: enhanced.cpp oslink.h dodgame.h parser.h enhanced.h dod.h
	$(CXX) $(CXXFLAGS) enhanced.cpp

object.o: object.cpp object.h dodgame.h parser.h oslink.h dod.h
	$(CXX) $(CXXFLAGS) object.cpp

oslink.o: oslink.cpp oslink.h dodgame.h viewer.h sched.h player.h dungeon.h parser.h object.h creature.h enhanced.h dod.h
	$(CXX) $(CXXFLAGS) oslink.cpp

parser.o: parser.cpp parser.h viewer.h dod.h
	$(CXX) $(CXXFLAGS) parser.cpp

player.o: player.cpp player.h dodgame.h viewer.h sched.h parser.h object.h dungeon.h creature.h oslink.h enhanced.h dod.h
	$(CXX) $(CXXFLAGS) player.cpp

sched.o: sched.cpp sched.h player.h viewer.h oslink.h creature.h parser.h dodgame.h dungeon.h object.h dod.h
	$(CXX) $(CXXFLAGS) sched.cpp

viewer.o: viewer.cpp viewer.h oslink.h player.h sched.h parser.h object.h dungeon.h creature.h enhanced.h dod.h
	$(CXX) $(CXXFLAGS) viewer.cpp

clean:
	@echo -n Cleaning...
	$(RM) $(OBJECTS)
	$(RM) $(OUTPUT)
	@echo Done

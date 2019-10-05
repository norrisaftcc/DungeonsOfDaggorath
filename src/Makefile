OBJECTS = creature.o dod.o dodgame.o dungeon.o enhanced.o object.o oslink.o parser.o player.o sched.o viewer.o


#CXX      = clang++-3.6
ifeq ($(OS),Windows_NT)
OUTPUT  = ../dod.html
CCLINK  = -lopengl32 -lmingw32 -lSDL2main -lSDL2 -mwindows -lSDL2_mixer
else
OUTPUT  = ../dod.html
#CCLINK  = -lGL -lSDL2 -lSDL2_mixer -s USE_SDL=2 -s USE_SDL_MIXER=2
#CCLINK  = -s USE_SDL=2 -s USE_SDL_MIXER=2 -s LEGACY_GL_EMULATION=1
#CCLINK  = -s USE_SDL=2 -s USE_SDL_MIXER=2 -s FULL_ES2=1
CCLINK  = -s USE_SDL=2 -s USE_SDL_MIXER=2 -s USE_REGAL=1 -s ALLOW_MEMORY_GROWTH=1 --preload-file ../assets@/ -s FULL_ES2=1 -s EMTERPRETIFY=1 -s EMTERPRETIFY_ASYNC=1 -s WASM=1 -s EXIT_RUNTIME=1
endif
#RM = rm
# -g is debug
CXXFLAGS = -std=c++11 -c -s USE_SDL=2 -s USE_SDL_MIXER=2 -s USE_REGAL=1 -s ALLOW_MEMORY_GROWTH=1 -s FULL_ES2=1 -s EMTERPRETIFY=1 -s EMTERPRETIFY_ASYNC=1 -s WASM=1 -s EXIT_RUNTIME=1

all: $(OUTPUT)

$(OUTPUT): $(OBJECTS)
	$(CXX) -o $(OUTPUT) $(OBJECTS) $(CCLINK)

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

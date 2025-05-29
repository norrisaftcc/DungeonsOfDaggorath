# Build Instructions

## Dependencies
- SDL2, SDL2_mixer
- OpenGL
- C++11 compiler

## Platform Builds

### macOS/Linux
```bash
brew install sdl2 sdl2_mixer  # macOS only
make
make clean
```

### Windows
```bash
make  # MinGW or use src/dod.dev with Dev-C++
```

### WebAssembly
```bash
cd src
emcc -o ../docs/index.html $(OBJECTS) -s USE_SDL=2 -O3 -s USE_SDL_MIXER=2 -s USE_REGAL=1 -s ALLOW_MEMORY_GROWTH=1 --preload-file ../assets@/ -s FULL_ES2=1 -s ASYNCIFY -s WASM=1 -s EXIT_RUNTIME=1 --shell-file standalone.html
```

## Output
- Native: `dod` (Unix/macOS) or `dod.exe` (Windows)
- Web: `docs/index.html` + `.js` + `.wasm`
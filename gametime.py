import time

_playing = False
_gameTime = 0
_timeOffset = 0

def GameTime():
    global _gameTime
    return _gameTime

def Update():
    global _gameTime
    global _timeOffset
    if IsPlaying():
        _gameTime = time.time() - _timeOffset

def IsPlaying():
    global _playing
    return _playing

def SetPlaying(playing):
    global _playing
    global _gameTime
    global _timeOffset
    if playing != _playing:
        _playing = playing
        if _playing:
            _timeOffset = time.time() - _gameTime
            
            

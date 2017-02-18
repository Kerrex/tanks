# Tanks
It is a 2D top-down shooter inspired mostly by [RecWar](http://recwar.50webs.com/) and [Battle City](https://en.wikipedia.org/wiki/Battle_City_%28video_game%29), although the gameplay is pretty different from them - some players noticed similarity to [Asteroids](https://en.wikipedia.org/wiki/Asteroids_%28video_game%29). You can control a simplistic circle-shaped tank firing round ricocheting bullets. Six types of guns and two types of chassis are available.

The game is not finished and probably will never be. It lacks many features, the most important ones in my opinion are:

* high quality graphics,
* configurable nicknames,
* map system,
* [lag compensation mechanism](http://gafferongames.com/networking-for-game-programmers/what-every-programmer-needs-to-know-about-game-networking/),
* support for multiple browsers - currently only Mozilla Firefox is supported.

The websocket server was written using Python and [Tornado](http://www.tornadoweb.org/en/stable/). The client uses HTML5, CSS and JavaScript.
Native client was written in [Godot Engine](https://godotengine.org/)

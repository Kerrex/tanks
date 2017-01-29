// main

// constants
var WIDTH = 480;
var HEIGHT = 480;

var TYPE_SPRITE = 0;
var TYPE_BULLET = 1;
var TYPE_CANNONBALL = 2;
var TYPE_ALPHA = 3;
var TYPE_LAMBDA = 4;
var TYPE_OBSTACLE = 5;

var TURRET_MONO = 0;
var TURRET_SOLI = 1;
var TURRET_DUO = 2;
var TURRET_OMNI = 3;
var TURRET_WIDER = 4;
var TURRET_BECKY = 5;

var MSGID_REGISTER = 1;
var MSGID_REGISTER_ACK = 2;
var MSGID_UPDATE = 3;
var MSGID_ACTION = 4;

var ACTID_MOTOR_ON = 1;
var ACTID_MOTOR_OFF = 2;
var ACTID_BRAKE_ON = 3;
var ACTID_BRAKE_OFF = 4;
var ACTID_FIRE_ON = 5;
var ACTID_FIRE_OFF = 6;
var ACTID_ROTATE_CL = 7;
var ACTID_ROTATE_CC = 8;
var ACTID_ROTATE_STOP = 9;

var STATUS_NOK = 0;
var STATUS_OK = 1;
// constants - end

// global functions
function roundedRect(ctx, x, y, width, height, radius) {
	ctx.beginPath();
	ctx.moveTo(x,y+radius);
	ctx.lineTo(x,y+height-radius);
	ctx.quadraticCurveTo(x,y+height,x+radius,y+height);
	ctx.lineTo(x+width-radius,y+height);
	ctx.quadraticCurveTo(x+width,y+height,x+width,y+height-radius);
	ctx.lineTo(x+width,y+radius);
	ctx.quadraticCurveTo(x+width,y,x+width-radius,y);
	ctx.lineTo(x+radius,y);
	ctx.quadraticCurveTo(x,y,x,y+radius);
	ctx.fill();
}

function logLast(str) {
	var place = document.getElementById("lastevent");
	place.innerHTML = str;
}
// global functions - end

// other variables
var ctx;
var last_key_down = null;
// other variables - end

// singletons
var sprites = [];
sprites.draw = function () {
	var i;
	ctx.clearRect(0, 0, WIDTH, HEIGHT);
	for (i = 0; i < sprites.length; ++i) {
		if (sprites[i] != undefined)
			sprites[i].draw();
	}
	window.requestAnimationFrame(sprites.draw);
}

var wsclient = {};
wsclient.send = function (msg) {
	var mesg = JSON.stringify(msg);
	this.socket.send(mesg);
	logLast("Message: " + mesg);
}
wsclient.register = function (nick) {
	var msg = new Message();
	msg.id = MSGID_REGISTER;
	msg.data = { "nick": nick };
	this.send(msg);
}
wsclient.act = function (action_id) {
	var msg = new Message();
	msg.id = MSGID_ACTION;
	msg.data = { "action_id": action_id };
	this.send(msg);
}
wsclient.init = function () {
	try {
		//this.socket = new WebSocket("ws://176.102.176.145:8080");
		this.socket = new WebSocket("ws://localhost:8080");
		//this.socket = new WebSocket("ws://echo.websocket.org");
		this.socket.onclose = function (close) {
			logLast("Socket: closed");
		}

		this.socket.onerror = function (error) {
			logLast("Socket: error");
		}

		this.socket.onmessage = function (message) {
			var msg = JSON.parse(message.data);
			logLast("Response: " + message.data);
			switch (msg.id) {
				case MSGID_REGISTER_ACK:
					// to be ignored for now
					break;
				case MSGID_UPDATE:
					var id = msg.data.id;
					if (msg.data.delete != undefined) {
						delete sprites[id];
					}
					else {
						if (sprites[id] == undefined) {
							sprites[id] = new Sprite();
						}
						sprites[id].x = msg.data.x || sprites[id].x;
						sprites[id].y = msg.data.y || sprites[id].y;
						sprites[id].r = msg.data.r || sprites[id].r;
						sprites[id].radius = msg.data.radius || sprites[id].radius;
						sprites[id].nick = msg.data.nick || sprites[id].nick;
						sprites[id].color = msg.data.color || sprites[id].color;
						sprites[id].type = msg.data.type || sprites[id].type;
						sprites[id].turret = msg.data.turret || sprites[id].turret;
					}
					// window.requestAnimationFrame(sprites.draw);
					// sprites.draw();
					break;
			}
		}

		this.socket.onopen = function (open) {
			logLast("Socket: open");
			wsclient.register("Player");
		}
	}
	catch (e) {
		window.alert(e);
	}
}
// singletons - end

// constructors
function Sprite() {
	this.x = WIDTH / 2;
	this.y = HEIGHT / 2;
	this.r = 0;
	this.type = TYPE_BULLET;
	this.turret = TURRET_MONO;
	this.color = "red";
	this.nick = "";
}

Sprite.prototype.draw = function () {
	var path = new Path2D();
	var x = this.x;
	var y = this.y;
	var r = this.r;
	var radius = this.radius;
	var color = this.color;
	var nick = this.nick;
	var type = this.type;
	var turret = this.turret;
	ctx.save();
	ctx.fillStyle = "black";
	if (color) {
		ctx.fillStyle = color;
	}
	ctx.translate(x, y);
	if (nick) {
		ctx.textAlign = "center";
		ctx.fillText(nick, 0, 16);
	}
	ctx.rotate(r);
	switch (type) {
		case TYPE_BULLET:
		case TYPE_CANNONBALL:
		case TYPE_OBSTACLE:
			path.arc(0, 0, radius, 0, 2 * Math.PI);
			ctx.fill(path);
			break;
		case TYPE_ALPHA:
		case TYPE_LAMBDA:
			// turret
			switch (turret) {
				case TURRET_MONO:
					roundedRect(ctx, -2, -16, 4, 14, 2);
					break;
				case TURRET_SOLI:
					roundedRect(ctx, -2, -22, 4, 20, 2);
					break;
				case TURRET_DUO:
					roundedRect(ctx, -5, -16, 4, 14, 2);
					roundedRect(ctx, 1, -16, 4, 14, 2);
					break;
				case TURRET_OMNI:
					ctx.save();
					roundedRect(ctx, -2, -16, 4, 14, 2);
					ctx.rotate(-Math.PI / 6);
					roundedRect(ctx, -1, -14, 2, 14, 2);
					ctx.rotate(-Math.PI / 6);
					roundedRect(ctx, -1, -12, 2, 14, 2);
					ctx.rotate(-Math.PI / 6);
					roundedRect(ctx, -2, -12, 4, 14, 2);
					ctx.rotate(-Math.PI / 6);
					roundedRect(ctx, -1, -12, 2, 14, 2);
					ctx.rotate(-Math.PI / 6);
					roundedRect(ctx, -1, -12, 2, 14, 2);
					ctx.rotate(-Math.PI / 6);
					roundedRect(ctx, -2, -12, 4, 14, 2);
					ctx.rotate(-Math.PI / 6);
					roundedRect(ctx, -1, -12, 2, 14, 2);
					ctx.rotate(-Math.PI / 6);
					roundedRect(ctx, -1, -12, 2, 14, 2);
					ctx.rotate(-Math.PI / 6);
					roundedRect(ctx, -2, -12, 4, 14, 2);
					ctx.rotate(-Math.PI / 6);
					roundedRect(ctx, -1, -12, 2, 14, 2);
					ctx.rotate(-Math.PI / 6);
					roundedRect(ctx, -1, -14, 2, 14, 2);
					ctx.restore();
					break;
				case TURRET_WIDER:
					ctx.save();
					roundedRect(ctx, -2, -16, 4, 14, 2);
					ctx.rotate(-Math.PI / 24);
					roundedRect(ctx, -4, -16, 2, 14, 2);
					ctx.rotate(Math.PI / 12);
					roundedRect(ctx, 2, -16, 2, 14, 2);
					ctx.restore();
					break;
				case TURRET_BECKY:
					ctx.save();
					roundedRect(ctx, -2, -16, 4, 14, 2);
					ctx.rotate(11 * Math.PI / 12);
					roundedRect(ctx, -3, -14, 2, 14, 2);
					ctx.rotate(2 * Math.PI / 12);
					roundedRect(ctx, 1, -14, 2, 14, 2);
					ctx.restore();
					break;
			}
			// chassis
			path.arc(0, 0, radius, 0, 2 * Math.PI);
			ctx.fill(path);
			if (type == TYPE_LAMBDA) {
				ctx.save();
				ctx.fillStyle = "white";
				path2 = new Path2D();
				path2.arc(0, 0, radius / 2, 0, 2 * Math.PI);
				ctx.fill(path2);
				ctx.restore();
			}
			break;
			/*
		case TYPE_TANK_2:
			path.arc(0, 0, radius, 0, 2 * Math.PI);
			ctx.fill(path);
			ctx.rotate(-Math.PI / 24);
			roundedRect(ctx, -4, -16, 3, 14, 2);
			ctx.rotate(Math.PI / 12);
			roundedRect(ctx, 0, -16, 3, 14, 2);
			break;
		case TYPE_TANK_3:
			path.arc(0, 0, radius, 0, 2 * Math.PI);
			ctx.fill(path);
			roundedRect(ctx, -2, -16, 3, 14, 2);
			ctx.rotate(-Math.PI / 24);
			roundedRect(ctx, -5, -16, 3, 14, 2);
			ctx.rotate(Math.PI / 12);
			roundedRect(ctx, 1, -16, 3, 14, 2);
			break;
			*/
	}
	ctx.restore();
}

function Message() {
	this.id = 0;
	this.data = {};
}
// constructors - end

function init() {
	var canvas = document.getElementById("gamescreen");
	if (canvas.getContext) {
		ctx = canvas.getContext("2d");
	}
	else {
		window.alert("Canvas tag not supported.");
	}
	wsclient.init();
	window.requestAnimationFrame(sprites.draw);
}

function keydownservice(ev) {
	if (last_key_down != ev.code) {
		switch (ev.code) {
			case "KeyA":
			case "KeyJ":
			case "ArrowLeft":
				wsclient.act(ACTID_ROTATE_CC);
				break;
			case "KeyW":
			case "KeyI":
			case "ArrowUp":
				wsclient.act(ACTID_MOTOR_ON);
				break;
			case "KeyS":
			case "KeyK":
			case "ArrowDown":
				wsclient.act(ACTID_BRAKE_ON);
				break;
			case "KeyD":
			case "KeyL":
			case "ArrowRight":
				wsclient.act(ACTID_ROTATE_CL);
				break;
			case "Space":
			case "KeyZ":
			case "KeyX":
				wsclient.act(ACTID_FIRE_ON);
				break;
			default:
				break;
		}
	}
	last_key_down = ev.code;
}

function keyupservice(ev) {
		switch (ev.code) {
		case "KeyA":
		case "KeyJ":
		case "ArrowLeft":
			wsclient.act(ACTID_ROTATE_STOP);
			break;
		case "KeyW":
		case "KeyI":
		case "ArrowUp":
			wsclient.act(ACTID_MOTOR_OFF);
			break;
		case "KeyS":
		case "KeyK":
		case "ArrowDown":
			wsclient.act(ACTID_BRAKE_OFF);
			break;
		case "KeyD":
		case "KeyL":
		case "ArrowRight":
			wsclient.act(ACTID_ROTATE_STOP);
			break;
		case "Space":
		case "KeyZ":
		case "KeyX":
			wsclient.act(ACTID_FIRE_OFF);
			break;
		default:
			break;
	}
	last_key_down = null;
}

window.onload = init;
window.onkeydown = keydownservice;
window.onkeyup = keyupservice;

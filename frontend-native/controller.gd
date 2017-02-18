extends Node

# class member variables go here, for example:
# var a = 2
# var b = "textvar"
var ws_constants
var event
var webclient

func _ready():
	webclient = preload('webclient.gd').new()
	#webclient.initialize()
	ws_constants = preload('connection_constants.gd')
	set_process_input(true)
	
func _input(event):
	if event.is_action_pressed("accelerate"):
		webclient.act(ws_constants.ACTID_MOTOR_ON)
	elif event.is_action_pressed('brake'):
		webclient.act(ws_constants.ACTID_BRAKE_ON)
	elif event.is_action_pressed('turn_right'):
		webclient.act(ws_constants.ACTID_ROTATE_CL)
	elif event.is_action_pressed('turn_left'):
		webclient.act(ws_constants.ACTID_ROTATE_CC)
	elif event.is_action_released("accelerate"):
		webclient.act(ws_constants.ACTID_MOTOR_OFF)
	elif event.is_action_released("brake"):
		webclient.act(ws_constants.ACTID_BRAKE_OFF)
	elif event.is_action_released("turn_right"):
		webclient.act(ws_constants.ACTID_ROTATE_STOP)
	elif event.is_action_released("turn_left"):
		webclient.act(ws_constants.ACTID_ROTATE_STOP)
	elif event.is_action_pressed("fire"):
		webclient.act(ws_constants.ACTID_FIRE_ON)
	elif event.is_action_released("fire"):
		webclient.act(ws_constants.ACTID_FIRE_OFF)
	


extends Node2D

# class member variables go here, for example:
# var a = 2
# var b = "textvar"
var websocket
var constants

func _on_message(msg):
	pass
	#print(msg)
	#get_node("Label").set_text(msg)

func _init():
	print('Starting webclient')
	constants = preload('connection_constants.gd')
	websocket = preload('lib/websocket.gd').new(self)
	websocket.start('127.0.0.1', 8080)
	websocket.set_reciever(self, '_on_message')
	register("Tomek")
	
### msg - Dictionary type ###
func _send(msg):
	var message_in_str = msg.to_json()
	websocket.send(message_in_str)
	print('Message: ' + message_in_str + ' sent.')
	
func register(nickname):
	var msg = {"id": constants.MSGID_REGISTER, "data": {"nick": nickname} }
	_send(msg)
	
func act(action):
	var msg = {"id": 4, "data": {"action_id": action} }
	_send(msg)
	 
	

	



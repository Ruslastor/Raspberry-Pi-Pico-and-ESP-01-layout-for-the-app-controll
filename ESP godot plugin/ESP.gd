@icon("res://RaspberryTCP/iot.png")
class_name RaspberryTCP
extends Node

signal got_data(command : String, data : String)

var server : TCPServer = TCPServer.new()
var board : StreamPeerTCP

var previous_data : StringName = ''


func listen_to(port : int) -> void:
	server.listen(port)

func send(command : String, data : String, force_send : bool = false) -> void:
	if self.board:
		if force_send or self.previous_data != data:
			self.board.put_data(str(command+'|'+data).to_utf8_buffer())
			self.board.poll()

func _process(_delta : float) -> void:
	if self.board:
		var avb : int = self.board.get_available_bytes()
		if avb > 0:
			var data = self.board.get_data(avb)[1]
			if data:

				var data_array : PackedStringArray = PackedByteArray(data).get_string_from_utf8().split('|')
				if len(data_array) > 1:
					emit_signal('got_data', data_array[0], data_array[1])
		self.board.poll()
	else:
		self.board = self.server.take_connection()
